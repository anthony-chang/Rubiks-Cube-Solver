from sys import stdin, stdout
from math import *
import imutils
from imutils import contours
import cv2
import numpy as np

url = 'https://192.168.137.216:8080/'
feed = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#feed = cv2.VideoCapture(url+'video')
FEED_WIDTH = int(feed.get(3))
FEED_HEIGHT = int(feed.get(4))

cv2.namedWindow('Feed', cv2.WINDOW_AUTOSIZE)
cv2.moveWindow('Feed', 0, 0)
cv2.namedWindow('Mask', cv2.WINDOW_AUTOSIZE)
cv2.moveWindow('Mask', FEED_WIDTH, 0)
# cv2.namedWindow('Cube', cv2.WINDOW_AUTOSIZE)
# cv2.moveWindow('Cube', FEED_WIDTH, 0)

squares1 = [[(0, 0) for i in range(2)] for y in range(9)]
squares2 = [[(0, 0) for i in range(2)] for y in range(9)]
colours = [(0, 0, 255) for i in range(9)]
canvas = np.zeros(shape=[250, 300, 3], dtype=np.uint8)

for i in range(9):
    squares1[i][0] = (150 + (i % 3) * 90, 100 + (i // 3) * 90)
    squares1[i][1] = (235 + (i % 3) * 90, 185 + (i // 3) * 90)
    squares2[i][0] = (80 + (i % 3) * 25, 50 + (i // 3) * 25)
    squares2[i][1] = (130 + (i % 3) * 45, 100 + (i // 3) * 45)

while (1):
    # Capture frame-by-frame
    (ret, frame) = feed.read()
    # frame = cv2.flip(frame,1) #mirror the stream

    # Draw the nine squares to align the cube
    for i in range(9):
        cv2.rectangle(frame, squares1[i][0], squares1[i][1], (255, 255, 255), 1)
        #cv2.rectangle(canvas, squares2[i][0], squares2[i][1], colours[i], -1)
        #cv2.putText(frame, str(i+1), tuple(np.add(squares1[i][0], (0, 10))), cv2.FONT_HERSHEY_PLAIN, 0.8, (255, 255, 255))

    colourMask = [0 for i in range(6)]
    # frame = np.concatenate((frame, canvas), axis=1)
    framehsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    colourMask[0] = cv2.inRange(framehsv, (15, 90, 130), (60, 245, 245))  # yellow
    colourMask[1] = cv2.inRange(framehsv, (70, 20, 130), (180, 110, 255))  # white
    colourMask[2] = cv2.inRange(framehsv, (80, 180, 140), (120, 255, 255))  # blue
    colourMask[3] = cv2.inRange(framehsv, (5, 70, 150), (15, 235, 255))  # orange
    colourMask[4] = cv2.inRange(framehsv, (60, 110, 110), (100, 220, 250))  # green
    colourMask[5] = cv2.inRange(framehsv, (0, 110, 165), (5, 255, 255))  # red

    mask = colourMask[0]
    for i in range(6):
        mask = cv2.bitwise_or(mask, colourMask[i])

    mask = mask[100:365, 150:415] #Crop the mask
    cntsUnfiltered = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntsUnfiltered = cntsUnfiltered[0] if len(cntsUnfiltered) == 2 else cntsUnfiltered[1]

    cnts = []
    for i in range(len(cntsUnfiltered)):
        if cv2.contourArea(cntsUnfiltered[i]) > 3000 and cv2.contourArea(cntsUnfiltered[i]) < 8000:
            cnts.append(cntsUnfiltered[i])


    # Sort all contours from top-to-bottom or bottom-to-top
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:9]  # Sort 9 largest contours
    if len(cnts) > 0:
        (cnts, _) = contours.sort_contours(cnts, method="top-to-bottom")


    # Take each row of 3 and sort from left-to-right or right-to-left
    cube_rows = []
    row = []
    for (i, c) in enumerate(cnts, 1):
        row.append(c)
        if i % 3 == 0:
            (cnts, _) = contours.sort_contours(row, method="left-to-right")
            cube_rows.append(cnts)
            row = []

    number = 0
    for row in cube_rows:
        for c in row:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x+150, y+100), (x + w+150, y + h+100), (36, 255, 12), 2)

            cv2.putText(frame, "#{}".format(number + 1), (x+150, y+100 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            #cv2.putText(frame, str(w*h), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            number += 1
            if number > 9:
                break
        if number > 9:
            break

    cv2.imshow('Feed', frame)
    cv2.imshow('Mask', mask)
    # cv2.imshow('Cube', canvas)

    if cv2.waitKey(10) & 0xFF == 27:
        break

# When everything done, release the capture
feed.release()
cv2.destroyAllWindows()
