from sys import stdin, stdout
from math import *
from imutils import contours
import cv2
import numpy as np

url = 'https://192.168.137.216:8080/'
feed = cv2.VideoCapture(0, cv2.CAP_DSHOW)
feed.open(0)
# feed = cv2.VideoCapture(url+'video')
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

OFFSET = squares1[0][0]


def findcolour(xx, yy, ww, hh):
    avg = []
    maxVal = 0
    maxColour = -1
    for k in range(6):
        avg.append(0)
        for i in range(ww):
            for j in range(hh):
                avg[k] += colourMask[k][xx + i + OFFSET[0]][yy + j + OFFSET[1]]
        avg[k] = avg[k] / (ww * hh)
        if avg[k] > maxVal:
            maxVal = avg[k]
            maxColour = k
    return maxColour


def num2colour(num):
    if num == 0:
        return "yellow"
    if num == 1:
        return "white"
    if num == 2:
        return "blue"
    if num == 3:
        return "orange"
    if num == 4:
        return "green"
    if num == 5:
        return "red"


while 1:
    # Capture frame-by-frame
    (ret, frame) = feed.read()
    # frame = cv2.flip(frame,1) #mirror the stream

    # Draw the nine squares to align the cube
    for i in range(9):
        cv2.rectangle(frame, squares1[i][0], squares1[i][1], (255, 255, 255), 1)
        # cv2.rectangle(canvas, squares2[i][0], squares2[i][1], colours[i], -1)
        # cv2.putText(frame, str(i+1), tuple(np.add(squares1[i][0], (0, 10))), cv2.FONT_HERSHEY_PLAIN, 0.8, (255, 255, 255))

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

    mask = mask[OFFSET[1]:365, OFFSET[0]:415]  # Crop the mask
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

    # Print the bounding rectangles and number them
    number = 0
    for row in cube_rows:
        for c in row:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x + OFFSET[0], y + OFFSET[1]), (x + w + OFFSET[0], y + h + OFFSET[1]), (36, 255, 12),
                          2)
            cv2.putText(frame, "#{}".format(number + 1), (x + OFFSET[0], y + OFFSET[1] - 5), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (255, 255, 255), 2)
            number += 1
            if number > 9:
                break
        if number > 9:
            break

    if cv2.waitKey(10) & 0xFF == 10:
        num = 1
        for row in cube_rows:
            for c in row:
                x, y, w, h = cv2.boundingRect(c)
                print(num2colour(findcolour(x, y, w, h)) + ', ')
                num += 1
            if num > 9:
                break
        if num > 9:
            break



    cv2.imshow('Feed', frame)
    cv2.imshow('Mask', colourMask[1])
    # cv2.imshow('Cube', canvas)

# When everything done, release the capture
feed.release()
cv2.destroyAllWindows()
