# Creator: Ian Zalewski on 25.6.2026
# For: Research with Proffesor Andrea Dernbecher
# Purpose: Use indivual image segmenter to go through folder of images

from individualImageSegmenter import segment_image
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os 
import csv
from tkinter import filedialog
import timeStamps
import pandas as pd


#Pick file, opens file browser to point to file for analysis
def openFileBrowser():
    Tk().withdraw() 
    fileName = askopenfilename() 
    print(fileName)
    return fileName


def segmentFolder(mainFolderPath, shape, csvName = "meWhen", callback=None):
    
    silTimestamp, phosTimeStamps, folderPathSilhouette, folderPathPhosphor = timeStamps.getAllTimeStamps(mainFolderPath)

    #create arrays to be appended to
    
    lengthSL = []
    heightSL = []
    areaSL = [] 

    widthPL = []
    heightPL = []
    areaPL = []


    #Create file path for output csv
    csvName = csvName + ".csv"

    #Uses os to go through and find folder with image files in it
    for e in os.scandir(folderPathSilhouette):
        try:
            if e.is_file():
                areaS, lengthS, heightS, result_img = segment_image(e.path, shape)

                areaSL.append(areaS)
                lengthSL.append(lengthS)
                heightSL.append(heightS)

                callback(result_img, 1)
        except Exception as e: 
            print("Attempt Failed:")

    #Go through folder of phosphor photos
    for e in os.scandir(folderPathPhosphor):
        try:
            if e.is_file():
                areaP, widthP, heightP, result_img = segment_image(e.path, shape)

                widthPL.append(widthP)
                heightPL.append(heightP)
                areaPL.append(areaPL)

                callback(result_img, 2)
        except Exception as e: 
            print("Attempt Failed:")


    dfSilhouette = pd.DataFrame({"Timestamp": silTimestamp, "Area_Sil": areaS, "Length_Sil": lengthS, "Height_Sil": heightS})
    dfPhosphor = pd.DataFrame({"Timestamp": phosTimeStamps,"Area_Phos": areaP,"Width_Phos": widthP, "Height_Phos": heightP})

    dfSilhouette = dfSilhouette.sort_values("Timestamp").reset_index(drop=True)
    dfPhosphor = dfPhosphor.sort_values("Timestamp").reset_index(drop=True)

    mergedDf = pd.merge_asof(dfPhosphor,dfSilhouette, on="Timestamp", direction="nearest", tolerance=pd.Timedelta(seconds=2))

    mergedDf.to_csv(csvName, index=False)
        

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