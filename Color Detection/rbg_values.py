import cv2


def rgb(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:  # checks mouse moves
        #colorsBGR = image[y, x]
        #colorsRGB = tuple(reversed(colorsBGR))  # Reversing the OpenCV BGR format to RGB format
        colourHSV = imagehsv[y, x]
        #print("RGB Value at ({},{}):{} ".format(x, y, colorsRGB))
        cv2.rectangle(image, (0, 0), (140, 30), (255, 255, 255), -1)
        cv2.putText(image, str(colourHSV), (10, 20), cv2.FONT_HERSHEY_PLAIN, 0.9, 0)


# Read an image
image = cv2.resize(cv2.imread("1.jpg"), (500, 500))
imagehsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Create a window and set Mousecallback to a function for that window
cv2.namedWindow('thing', cv2.WINDOW_NORMAL)
cv2.moveWindow('thing', 20, 20)
cv2.setMouseCallback('thing', rgb)

# Do until esc pressed
while (1):
    cv2.imshow('thing', image)
    if cv2.waitKey(10) & 0xFF == 27:
        break

# if esc is pressed, close all windows.
cv2.destroyAllWindows()