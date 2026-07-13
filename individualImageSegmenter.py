# Creator: Ian Zalewski on 8.6.2026
# For: Research with Proffesor Andrea Dernbecher
# Purpose: Take in image of particle and estimates size of particle

import cv2
import numpy as np
from math import pi, sqrt, pow
import csv
from PIL import Image
from tkinter.filedialog import askopenfilename
import tkinter as Tk




def distance(A, B):
    return sqrt((pow(A[0] + B[0], 2)) + (pow(A[1] + B[1], 2)))

def choppedContour(cnt, clean_mask, offSet):
     # Get bounding rectangle of the object
    x, y, w, h = cv2.boundingRect(cnt)
        
    #Finds the height of the top 15% of the image. Top 15% is cut off to remove the large protrusion from wire holding the particle
    top_offset = int(h * offSet)
        
    # Create a clean ROI (Region of Interest) mask
    clean_roi = np.zeros_like(clean_mask)
    # Only copy the bottom portion of the object into the clean mask
    clean_roi[y + top_offset : y + h, x : x + w] = clean_mask[y + top_offset : y + h, x : x + w]
        
    #Using the new image with the cut off wire, find new contour for the particle
    new_contours, _ = cv2.findContours(clean_roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return new_contours

#Function for segmenting the circle, giving outline and dimensions of particle
def segment_image(image_path, shape = "Circle", type="Highspeed"):

    #Sets size of kernel used for cleaning up image 
    if type == "Highspeed":
        kernelSize = 90
    else:
        kernelSize = 15

    #Sets image to grayscale, makes it easier for contouring to be done
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    #Inverts colors of the the image, uses algorithm to determine best values
    if type == "Highspeed":
        _, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    else: 
        _, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
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

    area = -1
    length = -1
    width = -1

    if type == "Highspeed":
        new_contours = choppedContour(cnt, clean_mask, 0.15)
    else:
        new_contours = choppedContour(cnt, clean_mask, 0)

    if(shape == "Circle"):

        if new_contours:
        #Use fitEllipse to find and draw a blue ellipse around the particle. From testing has been very accurate, though consult with proffesor for accuracy
            best_ellipse = cv2.fitEllipse(new_contours[0])
            cv2.ellipse(result_img, best_ellipse, (255, 0, 0), 3)
    
    # Display results from the coordinates of the ellipse found
        length = best_ellipse[1][0]
        width = best_ellipse[1][1]

    #Area equation if pi*(length/2)*(width/2)
        area = (pi/4) * length * width

    elif(shape == "Rectangle"):

        #Find the minimum area rectangle as a from the first contour. This allows for rotated rectangles
        rect = cv2.minAreaRect(new_contours[0])
        #Turns into usable lists for drawing on image
        box = cv2.boxPoints(rect)
        box = box.astype(int)
        cv2.drawContours(result_img, [box], 0, (0,0,255),2)

        #Calculates distanecs between top left and bottom left and top left and top right point to get side lengths
        height = int(distance(box[0], box[1]))
        length = int(distance(box[0], box[2]))

        area = height * length



    #result_img = convertImageToPILImage(result_img)

    return area, length, width, result_img
    

def convertImageToPILImage(img):
    color_converted = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result_img=Image.fromarray(color_converted)

    result_img = result_img.resize((200,200))

    return result_img

if __name__ == "__main__": 

    fileName = askopenfilename() 
    area, length, width, img = segment_image(fileName, "Rectangle", type="Phosphor")

    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 

    
