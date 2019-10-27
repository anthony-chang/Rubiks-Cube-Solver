from sys import stdin, stdout
from math import *
import cv2
import numpy as np


feed = cv2.VideoCapture(0)
FEED_WIDTH = int(feed.get(3));
FEED_HEIGHT = int(feed.get(4));


cv2.namedWindow('frame', cv2.WINDOW_AUTOSIZE)
cv2.moveWindow('frame', 20, 20)

squares = [[(0, 0) for i in range(2)] for y in range(9)]
canvas = np.zeros(shape=[FEED_HEIGHT, FEED_WIDTH-400, 3], dtype=np.uint8)
for i in range(9):
    squares[i][0] = (150+(i%3)*90, 100+(i//3)*90)
    squares[i][1] = (235+(i%3)*90, 185+(i//3)*90)
    print(str(squares[i][0]))


while(1):
    # Capture frame-by-frame
    (ret,frame) = feed.read()
    #frame = cv2.flip(frame,1) #mirror the stream

    #Draw the nine squares to align the cube
    for i in range(9):
        cv2.rectangle(frame, squares[i][0], squares[i][1], (255, 255, 255), 1)

    frame = np.concatenate((frame, canvas), axis=1)
    cv2.imshow('frame',frame)

    if cv2.waitKey(10) & 0xFF == 27:
        break

# When everything done, release the capture
feed.release()
cv2.destroyAllWindows()