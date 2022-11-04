import cv2
import logging

# simple logger
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(logging.FileHandler('image.log'))


# empty function for trackbar
def nothing(x):
    pass


# pass image to opencv and create several copies for drawing
path_to_image = './photo_2022-11-02_11-22-47.jpg'
image = cv2.imread(path_to_image)
cv2.namedWindow('image')
cv2.createTrackbar('alpha', 'image', 0, 255, nothing)
cv2.setTrackbarPos('alpha', 'image', 123)



#TODO: доработать
image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)

overlay = image.copy()
output = image.copy()
crop_img = None

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


# ---
def BrightnessContrast(brightness=0):
    global crop_img
    # getTrackbarPos returns the current
    # position of the specified trackbar.
    brightness = cv2.getTrackbarPos('Brightness',
                                    'cropped')

    contrast = cv2.getTrackbarPos('Contrast',
                                  'cropped')

    effect = controller(crop_img, brightness,
                        contrast)

    # The function imshow displays an image
    # in the specified window
    #cv2.imshow('Effect', effect)
    #cv2.imshow('cropped', effect)
    return effect


def controller(img, brightness=255,
               contrast=127):
    brightness = int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255))
    contrast = int((contrast - 0) * (127 - (-127)) / (254 - 0) + (-127))
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            max = 255
        else:
            shadow = 0
            max = 255 + brightness
        al_pha = (max - shadow) / 255
        ga_mma = shadow
        # The function addWeighted calculates
        # the weighted sum of two arrays
        cal = cv2.addWeighted(img, al_pha, img, 0, ga_mma)
    else:
        cal = img
    if contrast != 0:
        Alpha = float(131 * (contrast + 127)) / (127 * (131 - contrast))
        Gamma = 127 * (1 - Alpha)
        # The function addWeighted calculates
        # the weighted sum of two arrays
        cal = cv2.addWeighted(cal, Alpha, cal, 0, Gamma)
    return cal
# ---


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
        if crop_img is not None:
            cv2.destroyWindow("cropped")
            crop_img = None
        else:
            break
    elif key == 99:  # c - crop
        # create new window with cropped image
        if start_x != -1 and ((end_x-start_x)**2 + (end_y-start_y)**2 > 50):
            crop_img = image[start_y:end_y, start_x:end_x]
        else:
            crop_img = image.copy()
        crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)  # change color to gray
        #crop_img = cv2.GaussianBlur(crop_img, (5, 5), 0)  # add blur
        #crop_img = cv2.Canny(crop_img, 75, 200)  # change color to gray
        cv2.imshow("cropped", crop_img)
        cv2.createTrackbar('Brightness','cropped', 255, 2 * 255, BrightnessContrast)
        cv2.createTrackbar('Contrast', 'cropped', 127, 2 * 127, BrightnessContrast)
    elif key == ord('s') and crop_img is not None:
        cv2.imwrite(f'./{path_to_image.split("/")[-1].split(".")[0]}_scanned.jpg', BrightnessContrast(0))

    # --
    if crop_img is not None:
        #cv2.imshow("cropped", crop_img)
        cv2.imshow('cropped', BrightnessContrast(0))

cv2.destroyAllWindows()  # destroys the window showing image


#add black&white