from skimage.filters import threshold_local
import numpy as np
import cv2
import logging
import imutils

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(logging.FileHandler('image.log'))


def nothing(x):
    pass


image = cv2.imread('image.jpg')
cv2.namedWindow('image')
cv2.createTrackbar('alpha', 'image', 0, 255, nothing)

overlay = image.copy()
output = image.copy()

rect = []  # list of coordinates

drawing = False
start_x, start_y = -1, -1


# mouse callback function
def draw(event, x, y, flags, param):
    global start_x, start_y, drawing, image, overlay, output
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_x, start_y = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            # cv.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
            cv2.rectangle(overlay, (start_x, start_y), (x, y), (200, 65, 65), -1)  # A filled rectangle
            alpha = cv2.getTrackbarPos('alpha',
                                       'image') / 255  # Transparency factor. Get from trackbar and map to [0,1]
            # Following line overlays transparent rectangle over the image
            cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, output)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(overlay, (start_x, start_y), (x, y), (200, 65, 65), -1)  # A filled rectangle


def mouse_click(event, x, y,
                flags, param):
    # to check if left mouse
    # button was clicked
    if event == cv2.EVENT_LBUTTONCLK:
        # font for left click event
        print('click')


cv2.setMouseCallback('image', draw)

while True:
    cv2.imshow('image', output)
    key = cv2.waitKey(1)
    log.info(key)
    # print(key)
    alpha = cv2.getTrackbarPos('alpha', 'image') / 255
    cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, output)

    if key == 32:  # space
        #  delete all drawings
        overlay = image.copy()
        output = image.copy()
    elif key == 27:  # esc
        break

cv2.destroyAllWindows()  # destroys the window showing image

# TODO:
# сделать возможность рисовать только один rect и сохранять его координате, если не нравится -> перерисовать, иначе
# добавить кнопку, которая отвечает за обрезание фотографии
