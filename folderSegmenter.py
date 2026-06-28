from individualImageSegmenter import segment_image
from individualImageSegmenter import openFileBrowser
import cv2
import os 
import csv
from tkinter import filedialog

def segmentFolder(folderPath, shape, csvName = "meWhen"):

    csvName = csvName + ".csv"

    with open(csvName, mode='w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow([shape, shape, shape])
        writer.writerow(["Area", "Length", "Width"])
    
        for e in os.scandir(folderPath):
    
            if e.is_file():
                area, length, width = segment_image(e, shape)
            
                writer.writerow([area, length, width])
    

        

                

def main():

    filePath = filedialog.askdirectory()
    shape = ""

    while shape != "Rectangle" and shape != "Circle":
        shape = input("Please enter Circle or Rectangle: ")

        if(shape != "Rectangle" and shape != "Circle"):
            print("Error, please input correct shape!")

    csvName = input("Enter CSV name: ")

    segmentFolder(filePath, shape, csvName)

if __name__ == "__main__":
    main()