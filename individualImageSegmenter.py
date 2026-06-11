# Creator: Ian Zalewski on 8.6.2026
# For: Research with Proffesor Andrea Dernbecher
# Purpose: Take in image of particle and estimates size of particle

from tkinter import Tk
from tkinter.filedialog import askopenfilename
import cv2
import numpy as np
from math import pi

#Pick file, opens file browser to point to file for analysis
Tk().withdraw() 
filename = askopenfilename() 
print(filename)

#Function for segmenting the circle, giving outline and dimensions of particle
def segment_circle(image_path):
    #Sets size of kernel used for cleaning up image 
    kernelSize = 90

    #Sets image to grayscale, makes it easier for contouring to be done
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    #Inverts colors of the the image, uses algorithm to determine best values
    _, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Creates structuring element used in removing the wires for the contouring
    # Uses an open morph which removes pixels from edge of objects then add them back in
    # This causes the thinner wires to dissapear while keeping particle intact
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernelSize, kernelSize))
    clean_mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    
    # Goes through and find the edges/countours 
    contours, _ = cv2.findContours(clean_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Create a color copy of the original image for drawing results
    result_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    #Takes the first contour the algorithm finds. The second one was larger in given test samples. Subject to change 
    cnt = contours[0]

    # Get bounding rectangle of the object
    x, y, w, h = cv2.boundingRect(cnt)
        
    #Finds the height of the top 15% of the image. Top 15% is cut off to remove the large protrusion from wire holding the particle
    top_offset = int(h * 0.15)
        
    # Create a clean ROI (Region of Interest) mask
    clean_roi = np.zeros_like(clean_mask)
    # Only copy the bottom portion of the object into the clean mask
    clean_roi[y + top_offset : y + h, x : x + w] = clean_mask[y + top_offset : y + h, x : x + w]
        
    #Using the new image with the cut off wire, find new contour for the particle
    new_contours, _ = cv2.findContours(clean_roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if new_contours:
        #Use fitEllipse to find and draw a blue ellipse around the particle. From testing has been very accurate, though consult with proffesor for accuracy
        best_ellipse = cv2.fitEllipse(new_contours[0])
        cv2.ellipse(result_img, best_ellipse, (255, 0, 0), 3)

    # Display results from the coordinates of the ellipse found
    lengthOfEllipse = best_ellipse[1][0]
    widthOfEllipse = best_ellipse[1][1]

    #Area equation if pi*(length/2)*(width/2)
    areaOfEllipse = (pi/4) * lengthOfEllipse * widthOfEllipse
    
    #Print details to terminal. Can be modified to write a csv
    print("Details of Best Fit Ellipse")  
    print("Area: ", areaOfEllipse, "\tLength: ", lengthOfEllipse,"\t Width: ", widthOfEllipse)      
    
    #Shows the segmented image with contour drawing. With video will be replaced with a segmented video
    cv2.imshow("Mask without wires", clean_mask)
    cv2.imshow("Segmented Result", result_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Run the function on selected file
segment_circle(filename)