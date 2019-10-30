import cv2
import numpy as np
from imutils import contours

url = 'https://192.168.137.230:8080/'
feed = cv2.VideoCapture(0, cv2.CAP_DSHOW)
feed.open(0)
#feed = cv2.VideoCapture(url+'video')
FEED_WIDTH = int(feed.get(3))
FEED_HEIGHT = int(feed.get(4))

squares1 = [[(0, 0) for i in range(2)] for y in range(9)]
squares2 = [[(0, 0) for i in range(2)] for y in range(9)]
outputColours = ["" for i in range(6)]
canvas = np.zeros(shape=[250, 300, 3], dtype=np.uint8)

for i in range(9):
    squares1[i][0] = (150 + (i % 3) * 90, 100 + (i // 3) * 90)
    squares1[i][1] = (235 + (i % 3) * 90, 185 + (i // 3) * 90)
    squares2[i][0] = (80 + (i % 3) * 45, 50 + (i // 3) * 45)
    squares2[i][1] = (120 + (i % 3) * 45, 90 + (i // 3) * 45)

OFFSET = squares1[0][0]

cv2.namedWindow('Feed', cv2.WINDOW_AUTOSIZE)
cv2.moveWindow('Feed', 0, 0)

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

    mask = framehsv[OFFSET[1]:365, OFFSET[0]:415]  # Crop the mask

    if cv2.waitKey(10) == ord('\r'):
        row_avg = np.average(mask, axis=0)
        avg = np.average(row_avg, axis=0)
        row_std = np.std(mask, axis=0)
        std = np.std(row_std, axis=0)
        print (avg)
        print (std)
    elif cv2.waitKey(10) & 0xFF == 27:
        break

    cv2.imshow('Feed', frame)

# Print the colours of the sides
for i in range(6):
    print(outputColours[i])

# When everything done, release the capture
feed.release()
cv2.destroyAllWindows()
