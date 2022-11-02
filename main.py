from skimage.filters import threshold_local
import numpy as np
import cv2
import imutils

image = cv2.imread('image.jpg')
cv2.imshow('sample img', image)
while True:
    key = cv2.waitKey(0)  # waits until a key is pressed
    if key == 27:  # esc
        break
cv2.destroyAllWindows()  # destroys the window showing image
