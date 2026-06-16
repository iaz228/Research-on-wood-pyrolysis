from individualImageSegmenter import segment_circle
from individualImageSegmenter import openFileBrowser
import cv2


def segmentVideo(cap):

    while(cap.isOpen() == True):
        ret, frame = cap.read()

        if(ret == True):
            segment_circle(frame)


def main():
    filePath = openFileBrowser()
    
    cap = cv2.VideoCapture(filePath)

    segmentVideo(cap)

if __name__ == "__main__":
    main()