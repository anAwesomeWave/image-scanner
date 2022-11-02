from skimage.filters import threshold_local
import numpy as np
import cv2
import logging
import imutils

# simple logger
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(logging.FileHandler('image.log'))


# empty function for trackbar
def nothing(x):
    pass

# pass image to opencv and create several copies for drawing
path_to_image = './image.jpg'
image = cv2.imread(path_to_image)
cv2.namedWindow('image')
cv2.createTrackbar('alpha', 'image', 0, 255, nothing)
cv2.setTrackbarPos('alpha', 'image', 123)

overlay = image.copy()
output = image.copy()

drawing = False  # for drawing (if True you can draw rect with moving)
can_draw = True  # allows draw only one rectangle

# coordinates of rectangle
start_x, start_y = -1, -1
end_x, end_y = -1, -1


# mouse callback function
def draw(event, x, y, flags, param):
    global start_x, start_y, drawing, can_draw, end_x, end_y
    if event == cv2.EVENT_LBUTTONDOWN and can_draw:  # start of drawing (user pressed left button)
        drawing = True
        start_x, start_y = x, y  # initialize parameters
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.rectangle(overlay, (start_x, start_y), (x, y), (200, 65, 65), -1)  # A filled rectangle
            alpha = cv2.getTrackbarPos('alpha',
                                       'image') / 255  # Transparency factor. Get from trackbar and map to [0,1]
            # Following line overlays transparent rectangle over the image
            cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, output)
    elif event == cv2.EVENT_LBUTTONUP:  # mouse up
        if can_draw:  # if it is the first rectangle
            drawing = False  # we are no longer drawing
            can_draw = False  # we can't draw another rect
            cv2.rectangle(overlay, (start_x, start_y), (x, y), (200, 65, 65), -1)  # A filled rectangle
            end_x, end_y = x, y  # get coords of mouse


cv2.setMouseCallback('image', draw)  # set callback func on mouse event

crop_img = None
while True:
    cv2.imshow('image', output)
    key = cv2.waitKey(1)
    # log.info(key)  # pass key into a  logger
    alpha = cv2.getTrackbarPos('alpha', 'image') / 255
    cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, output)  # always check alpha value and apply to rect

    if key == 32:  # space
        # reset (delete previous rectangle and allow draw another one)
        can_draw = True
        #  delete all drawings
        overlay = image.copy()
        output = image.copy()
    elif key == 27:  # esc (exit)
        break
    elif key == 99:  # c - crop
        # create new window with cropped image
        crop_img = image[start_y:end_y, start_x:end_x]
        crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)  # change color to gray
        cv2.imshow("cropped", crop_img)
    elif key == ord('s') and crop_img is not None:
        cv2.imwrite(f'./{path_to_image.split("/")[-1].split(".")[0]}_scanned.jpg', crop_img)

cv2.destroyAllWindows()  # destroys the window showing image
