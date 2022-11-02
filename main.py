from skimage.filters import threshold_local
import numpy as np
import cv2
import logging
import imutils

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(logging.FileHandler('image.log'))

image = cv2.imread('image.jpg')
cv2.namedWindow('image')

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
            cv2.rectangle(overlay, (start_x, start_y), (x, y), (0, 200, 0), -1)  # A filled rectangle
            alpha = 0.4  # Transparency factor.
            # Following line overlays transparent rectangle over the image
            cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, output)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        # cv.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
        cv2.rectangle(overlay, (start_x, start_y), (x, y), (0, 200, 0), -1)  # A filled rectangle
        alpha = 0.4  # Transparency factor.
        # Following line overlays transparent rectangle over the image
        cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, output)


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
    #print(key)

    if key == 32:  # space
        #  delete all drawings
        overlay = image.copy()
        output = image.copy()
    elif key == 27:  # esc
        break

cv2.destroyAllWindows()  # destroys the window showing image

# import numpy as np
# import cv2 as cv
#
# drawing = False  # true if mouse is pressed
# mode = True  # if True, draw rectangle. Press 'm' to toggle to curve
# ix, iy = -1, -1
#
#
# # mouse callback function
# def draw_circle(event, x, y, flags, param):
#     global ix, iy, drawing, mode, img
#     if event == cv.EVENT_LBUTTONDOWN:
#         drawing = True
#         ix, iy = x, y
#     elif event == cv.EVENT_MOUSEMOVE:
#         if drawing == True:
#             if mode == True:
#                 # cv.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
#                 cv.rectangle(overlay, (ix, iy), (x, y), (0, 200, 0), -1)  # A filled rectangle
#                 alpha = 0.4  # Transparency factor.
#                 # Following line overlays transparent rectangle over the image
#                 cv.addWeighted(overlay, alpha, img, 1 - alpha, 0, output)
#             else:
#                 cv.circle(img, (x, y), 5, (0, 0, 255), -1)
#     elif event == cv.EVENT_LBUTTONUP:
#         drawing = False
#         if mode == True:
#             # cv.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
#             cv.rectangle(overlay, (ix, iy), (x, y), (0, 200, 0), -1)  # A filled rectangle
#             alpha = 0.4  # Transparency factor.
#             # Following line overlays transparent rectangle over the image
#             cv.addWeighted(overlay, alpha, img, 1 - alpha, 0, output)
#         else:
#             cv.circle(img, (x, y), 5, (0, 0, 255), -1)
#
#
# img = cv.imread('image.jpg')
# overlay = img.copy()
# output = img.copy()
# # img = np.zeros((512,512,3), np.uint8)
# cv.namedWindow('image')
# cv.setMouseCallback('image', draw_circle)
# while (1):
#     cv.imshow('image', output)
#     k = cv.waitKey(1) & 0xFF
#     if k == ord('m'):
#         mode = not mode
#     elif k == 27:
#         break
# cv.destroyAllWindows()
