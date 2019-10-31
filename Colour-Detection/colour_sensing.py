import cv2
import numpy as np
from imutils import contours

url = 'https://10.42.0.18:8080/'
feed = cv2.VideoCapture(0, cv2.CAP_DSHOW)
feed.open(0)
feed = cv2.VideoCapture(url+'video')
FEED_WIDTH = int(feed.get(3))
FEED_HEIGHT = int(feed.get(4))

squares1 = [[(0, 0) for i in range(2)] for y in range(9)]
squares2 = [[(0, 0) for i in range(2)] for y in range(9)]
outputColours = ["" for i in range(6)]
canvas = np.zeros(shape=[250, 300, 3], dtype=np.uint8)

file = open("calib.txt", "r")
colourValues = []
for i in range(7):
    if (i == 0):
        file.readline()
        continue
    line = list(map(float, file.readline().strip().split(" ")))
    row = []
    maxVal = []
    maxVal.append(line[0])
    maxVal.append(line[1])
    maxVal.append(line[2])

    minVal = []
    minVal.append(line[3])
    minVal.append(line[4])
    minVal.append(line[5])

    row.append(minVal)
    row.append(maxVal)
    colourValues.append(row)

for i in range(9):
    squares1[i][0] = (150 + (i % 3) * 90, 100 + (i // 3) * 90)
    squares1[i][1] = (235 + (i % 3) * 90, 185 + (i // 3) * 90)
    squares2[i][0] = (80 + (i % 3) * 45, 50 + (i // 3) * 45)
    squares2[i][1] = (120 + (i % 3) * 45, 90 + (i // 3) * 45)

OFFSET = squares1[0][0]

cv2.namedWindow('Feed', cv2.WINDOW_AUTOSIZE)
cv2.moveWindow('Feed', 0, 0)
cv2.namedWindow('Mask', cv2.WINDOW_AUTOSIZE)
cv2.moveWindow('Mask', FEED_WIDTH, 0)
cv2.namedWindow('Cube', cv2.WINDOW_AUTOSIZE)
cv2.moveWindow('Cube', FEED_WIDTH, 300)


def findcolour(xx, yy, ww, hh):
    avg = []
    maxVal = 0
    maxColour = -1
    for k in range(6):
        avg.append(0)
        for i in range(ww):
            for j in range(hh):
                avg[k] += colourMask[k][yy + j][xx + i]
        avg[k] = avg[k] / (ww * hh)
        if avg[k] > maxVal:
            maxVal = avg[k]
            maxColour = k
    return maxColour


def num2colour(num):
    if num == 0:
        return "Y"
    if num == 1:
        return "W"
    if num == 2:
        return "B"
    if num == 3:
        return "O"
    if num == 4:
        return "G"
    if num == 5:
        return "R"


def colour2bgr(s):
    if s == "Y":
        return 0, 255, 255
    if s == "W":
        return 255, 255, 255
    if s == "B":
        return 255, 0, 0
    if s == "O":
        return 0, 140, 255
    if s == "G":
        return 0, 255, 0
    if s == "R":
        return 0, 0, 255

def getsidenum(s):
    if s == "R":
        return 0
    if s == "B":
        return 1
    if s == "G":
        return 2
    if s == "Y":
        return 3
    if s == "W":
        return 4
    if s == "O":
        return 5


while 1:
    # Capture frame-by-frame
    (ret, frame) = feed.read()
    # frame = cv2.flip(frame,1) #mirror the stream

    # Draw the nine squares to align the cube
    for i in range(9):
        cv2.rectangle(frame, squares1[i][0], squares1[i][1], (255, 255, 255), 1)
        cv2.rectangle(canvas, squares2[i][0], squares2[i][1], (255, 255, 255), 1)

    colourMask = [0 for i in range(6)]
    framehsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    colourMask[0] = cv2.inRange(framehsv, (colourValues[5][0][0], colourValues[5][0][1], colourValues[5][0][2]), (colourValues[5][1][0], colourValues[5][1][1], colourValues[5][1][2]))  # yellow
    colourMask[1] = cv2.inRange(framehsv, (colourValues[0][0][0], colourValues[0][0][1], colourValues[0][0][2]), (colourValues[0][1][0], colourValues[0][1][1], colourValues[0][1][2]))  # white
    colourMask[2] = cv2.inRange(framehsv, (colourValues[2][0][0], colourValues[2][0][1], colourValues[2][0][2]), (colourValues[2][1][0], colourValues[2][1][1], colourValues[2][1][2]))  # blue
    colourMask[3] = cv2.inRange(framehsv, (colourValues[3][0][0], colourValues[3][0][1], colourValues[3][0][2]), (colourValues[3][1][0], colourValues[3][1][1], colourValues[3][1][2]))  # orange
    colourMask[4] = cv2.inRange(framehsv, (colourValues[4][0][0], colourValues[4][0][1], colourValues[4][0][2]), (colourValues[4][1][0], colourValues[4][1][1], colourValues[4][1][2]))  # green
    colourMask[5] = cv2.inRange(framehsv, (colourValues[1][0][0], colourValues[1][0][1], colourValues[1][0][2]), (colourValues[1][1][0], colourValues[1][1][1], colourValues[1][1][2]))  # red

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

    coloursOnOneFace = ""
    if cv2.waitKey(10) == ord('\r'):
        num = 1
        for row in cube_rows:
            for c in row:
                x, y, w, h = cv2.boundingRect(c)
                colourLetter = num2colour(findcolour(x + OFFSET[0], y + OFFSET[1], w, h))
                strcolour = colour2bgr(colourLetter)
                cv2.rectangle(canvas, squares2[num - 1][0], squares2[num - 1][1], strcolour, -1)
                coloursOnOneFace += colourLetter
                num += 1
            if num > 9:
                break
    elif cv2.waitKey(10) & 0xFF == 27:
        break

    if len(coloursOnOneFace) == 9:
        outputColours[getsidenum(coloursOnOneFace[4])] = coloursOnOneFace


    cv2.imshow('Feed', frame)
    cv2.imshow('Mask', mask)
    cv2.imshow('Cube', canvas)

# Print the colours of the sides
for i in range(6):
    print(outputColours[i])

# When everything done, release the capture
feed.release()
cv2.destroyAllWindows()
