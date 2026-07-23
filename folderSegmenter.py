# Creator: Ian Zalewski on 25.6.2026
# For: Research with Proffesor Andrea Dernbecher
# Purpose: Use indivual image segmenter to go through folder of images

from individualImageSegmenter import segment_image
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os 
from pathlib import Path
from tkinter import filedialog
import timeStamps
import pandas as pd
from numpy import nan

VALID_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}

#Pick file, opens file browser to point to file for analysis
def openFileBrowser():
    Tk().withdraw() 
    fileName = askopenfilename() 
    print(fileName)
    return fileName


def segmentFolder(mainFolderPath, shape, csvName = "meWhen", callback=None):
    
    silTimestamp, phosTimeStamps, folderPathSilhouette, folderPathPhosphor, timePerImg = timeStamps.getAllTimeStamps(mainFolderPath)

    #create arrays to be appended to
    
    lengthSL = []
    heightSL = []
    areaSL = [] 

    widthPL = []
    heightPL = []
    areaPL = []


    #Create file path for output csv
    csvName = csvName + ".csv"

    sil_files = sorted([e for e in os.scandir(folderPathSilhouette)if e.is_file() and Path(e.path).suffix.lower() in VALID_EXTENSIONS], key=lambda x: x.name)
    phos_files = sorted([e for e in os.scandir(folderPathPhosphor)if e.is_file() and Path(e.path).suffix.lower() in VALID_EXTENSIONS],key=lambda x: x.name)

    #Uses os to go through and find folder with image files in it
    for e in sil_files:
        try:
            if e.is_file() and (Path(e.path).suffix.lower() in VALID_EXTENSIONS):
                print(e.path)
                areaS, lengthS, heightS, result_img = segment_image(e.path, shape, "Highspeed")

                areaSL.append(areaS)
                lengthSL.append(lengthS)
                heightSL.append(heightS)

                callback(result_img, 1)
        except Exception as e: 
            print("Attempt Failed:")
            areaSL.append(nan)
            lengthSL.append(nan)
            heightSL.append(nan)

    #Go through folder of phosphor photos
    for e in phos_files:
        try:
            if e.is_file() and (Path(e.path).suffix.lower() in VALID_EXTENSIONS):
                print(e.path)
                areaP, widthP, heightP, result_img = segment_image(e.path, shape, "Phosphor")

                widthPL.append(widthP)
                heightPL.append(heightP)
                areaPL.append(areaP)

                callback(result_img, 2)
        except Exception as exp: 
            print(exp)
            widthPL.append(nan)
            heightPL.append(nan)
            areaPL.append(nan)


    min_length_sil = min(len(silTimestamp), len(areaSL), len(lengthSL), len(heightSL))

    dfSilhouette = pd.DataFrame({"Timestamp": silTimestamp[:min_length_sil],"Area_Sil": areaSL[:min_length_sil],"Length_Sil": lengthSL[:min_length_sil],"Height_Sil": heightSL[:min_length_sil]})


    min_length_phos = min(len(phosTimeStamps), len(areaPL), len(widthPL), len(heightPL))

    dfPhosphor = pd.DataFrame({"Timestamp": phosTimeStamps[:min_length_phos],"Area_Phos": areaPL[:min_length_phos],"Width_Phos": widthPL[:min_length_phos],"Height_Phos": heightPL[:min_length_phos]})

    dfSilhouette = dfSilhouette.sort_values("Timestamp").reset_index(drop=True)
    dfPhosphor = dfPhosphor.sort_values("Timestamp").reset_index(drop=True)

    mergedDf = pd.merge_asof(dfSilhouette, dfPhosphor, on="Timestamp", direction="nearest", tolerance=pd.Timedelta(seconds=timePerImg - 0.0001))

    start_time = mergedDf["Timestamp"].iloc[0]
    mergedDf["Time_s"] = (mergedDf["Timestamp"] - start_time).dt.total_seconds().round(4)

    phosphor_cols = ["Area_Phos", "Width_Phos", "Height_Phos"]
    mergedDf[phosphor_cols] = mergedDf[phosphor_cols].fillna(-1)  

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