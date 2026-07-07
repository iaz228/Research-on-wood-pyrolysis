# Creator: Ian Zalewski on 25.6.2026
# For: Research with Proffesor Andrea Dernbecher
# Purpose: Use indivudla image segmenter to go through folder of images

from individualImageSegmenter import segment_image
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os 
import csv
from tkinter import filedialog


#Pick file, opens file browser to point to file for analysis
def openFileBrowser():
    Tk().withdraw() 
    fileName = askopenfilename() 
    print(fileName)
    return fileName


def segmentFolder(folderPath, shape, csvName = "meWhen"):

    #Create file path for output csv
    csvName = csvName + ".csv"


    #Opens new csv with file path name
    with open(csvName, mode='w', newline='') as file:
        writer = csv.writer(file)

        #Adds header rows 
        writer.writerow([shape, shape, shape])
        writer.writerow(["Area", "Length", "Width"])
    
        #Uses os to go through and find folder with image files in it
        for e in os.scandir(folderPath):
    
            if e.is_file():
                area, length, width = segment_image(e, shape)
            
                writer.writerow([area, length, width])
    

        

                

def main():

    #Pulls of directory dialog
    filePath = filedialog.askdirectory()
    shape = ""

    #Forces user to input correct shapes
    while shape != "Rectangle" and shape != "Circle":
        shape = input("Please enter Circle or Rectangle: ")

        if(shape != "Rectangle" and shape != "Circle"):
            print("Error, please input correct shape!")

    csvName = input("Enter CSV name: ")

    segmentFolder(filePath, shape, csvName)

if __name__ == "__main__":
    main()