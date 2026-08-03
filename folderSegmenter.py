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
from math import pi


VALID_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}

#Pick file, opens file browser to point to file for analysis
def openFileBrowser():
    Tk().withdraw() 
    fileName = askopenfilename() 
    print(fileName)
    return fileName


def segmentFolder(mainFolderPath, shape, csvName = "meWhen", frameSkipNumber = 1, chopAmount =0.12, dimension = 2, callback=None):
    
    startTime, timePerImg, phosTimeStamps, folderPathSilhouette, folderPathPhosphor = timeStamps.getAllTimeStamps(mainFolderPath)

    #create arrays to be appended to
    timeStampsSil = []

    lengthSL = []
    heightSL = []

    widthPL = []
    heightPL = []

    #Sort Folders so images are read in the correct orders
    sil_files = sorted([e for e in os.scandir(folderPathSilhouette)if e.is_file() and Path(e.path).suffix.lower() in VALID_EXTENSIONS], key=lambda x: x.name)
    phos_files = sorted([e for e in os.scandir(folderPathPhosphor)if e.is_file() and Path(e.path).suffix.lower() in VALID_EXTENSIONS],key=lambda x: x.name)

    
    numIterations = 0

    #Uses os to go through and find folder with image files in it
    for i, e in enumerate(sil_files):

        if(i % frameSkipNumber != 0):
            continue

        timeStampsSil.append(startTime + pd.Timedelta(seconds = i * timePerImg))
        
        
        try:
            if e.is_file() and (Path(e.path).suffix.lower() in VALID_EXTENSIONS):
                print(e.path)
                lengthS, heightS, result_img = segment_image(e.path, shape, chopAmount, "Highspeed")

                lengthSL.append(lengthS)
                heightSL.append(heightS)

                callback(result_img, 1)
        except Exception as e: 
            print(e)
            lengthSL.append(-1)
            heightSL.append(-1)

    #Go through folder of phosphor photos
    for e in phos_files:
        try:
            if e.is_file() and (Path(e.path).suffix.lower() in VALID_EXTENSIONS):
                print(e.path)
                widthP, heightP, result_img = segment_image(e.path, shape, "Phosphor")

                widthPL.append(widthP)
                heightPL.append(heightP)

                callback(result_img, 2)
        except Exception as exp: 
            print(exp)
            widthPL.append(-1)
            heightPL.append(-1)

    ##Area equation if pi*(length/2)*(width/2)
    #area = (pi/4) * length * width

    dfSilhouette = pd.DataFrame({"TimeStamp": timeStampsSil, "Length_Sil": lengthSL, "Height_Sil": heightSL})
    

    min_length_phos = min(len(phosTimeStamps), len(widthPL), len(heightPL))

    dfPhosphor = pd.DataFrame({"TimeStamp": phosTimeStamps[:min_length_phos],"Width_Phos": widthPL[:min_length_phos],"Height_Phos": heightPL[:min_length_phos]})

    dfSilhouette = dfSilhouette.sort_values("TimeStamp").reset_index(drop=True)
    dfPhosphor = dfPhosphor.sort_values("TimeStamp").reset_index(drop=True)

    mergedDf = pd.merge_asof(dfSilhouette, dfPhosphor, on="TimeStamp", direction="nearest", tolerance=pd.Timedelta(seconds=timePerImg))

    start_time = mergedDf["TimeStamp"].iloc[0]
    mergedDf["Time_s"] = (mergedDf["TimeStamp"] - start_time).dt.total_seconds().round(4)


    
    mergedDfPixels = mergedDf.copy()

    if shape == "Rectangle":
        mergedDfPixels["Volume"] = mergedDfPixels["Length_Sil"] * mergedDfPixels["Height_Sil"] * mergedDfPixels["Width_Phos"]
    elif shape == "Circle":
        mergedDfPixels["Volume"] = (4/3) * pi * mergedDfPixels["Length_Sil"] * mergedDfPixels["Height_Sil"] * mergedDfPixels["Width_Phos"]
    
    mergedDfPixels.to_csv(csvName + "inPixels.csv", index=False)




    mergedDfCM = mergedDf.copy()

    dataColumns = ["Length_Sil", "Height_Sil", "Width_Phos", "Height_Phos"]

    for entry in dataColumns:
        mergedDfCM[entry]= mergedDfCM[entry].apply(mapToCm, inputMax= mergedDfCM[entry].iloc[0], outputMax=dimension)

    if shape == "Rectangle":
        mergedDfCM["Volume"] = mergedDfCM["Length_Sil"] * mergedDfCM["Height_Sil"] * mergedDfCM["Width_Phos"]
    elif shape == "Circle":
        mergedDfCM["Volume"] = (4/3) * pi * mergedDfCM["Length_Sil"] * mergedDfCM["Height_Sil"] * mergedDfCM["Width_Phos"]

    mergedDfCM.to_csv(csvName + "inCM.csv", index=False)



def mapToCm(value, inputMax, outputMax):
    return (value * outputMax) / inputMax

