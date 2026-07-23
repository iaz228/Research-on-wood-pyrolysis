import pandas as pd
import os
from datetime import datetime
import re
from pathlib import Path

def getAllTimeStamps(folderPath):
    for e in os.scandir(folderPath):
        for file in os.scandir(e):
            if Path(file).suffix.lower() == ".txt":
                silTimeStamps = silTimeStampGetter(file)

            elif Path(file).suffix.lower() == ".xlsx":
                phosphorTimeStamps = getPhosphorTimeStamps(file)
    
    return silTimeStamps, phosphorTimeStamps




def silTimeStampGetter(file_path):
    with open(file_path, "r") as f:
        text = f.read()

    # 1. Extract Number of Images
    num_images_match = re.search(r"Number of images:\s*(\d+)", text)
    num_images = int(num_images_match.group(1)) if num_images_match else 0

    # 2. Extract Start Time string
    start_match = re.search(r"Start time:\s*(.+)", text)
    if start_match:
        start_time_raw = start_match.group(1).strip()
        start_time = pd.to_datetime(
            start_time_raw, format="%d %B %Y, %H:%M:%S.%f"
        )
    else:
        start_time = None

    # 3. Extract Average time interval (seconds per frame)
    interval_match = re.search(r"Average time interval between consecutive images:\s*([0-9.]+)", text)
    seconds_per_frame = (float(interval_match.group(1)) if interval_match else None)

    # 4. Generate list of pd.Timestamp objects for each frame
    if start_time is not None and seconds_per_frame is not None and num_images > 0:
        timestamps = [start_time + pd.Timedelta(seconds=i * seconds_per_frame) for i in range(num_images)]
    else:
        timestamps = []

    return timestamps


def getPhosphorTimeStamps(file_path):
   
    # Load Excel file
    df = pd.read_excel(file_path)

    # Clean rows to only include valid frame entries
    clean_df = df.dropna(subset=["No", "Time [s]"]).copy()

    # Combine Date column and Time [Timestamp] column into full Datetime objects
    date_str = clean_df["Date"].iloc[0].strftime("%Y-%m-%d")
    timestamps = pd.to_datetime(date_str + " " + clean_df["Time [Timestamp]"].astype(str)).tolist()

    return timestamps