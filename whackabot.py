# https://www.classicgame.com/game/Whack+a+Mole

# imports
import cv2
import pyautogui
from time import sleep, time
import numpy as np

# No cooldown time
pyautogui.PAUSE = 0
method = cv2.TM_CCOEFF_NORMED
threshold = 0.8

# template and dimensions
template = cv2.imread("imgs/nose.png")
template_gray = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)
template_w, template_h = template_gray.shape[::-1]
top_left = cv2.imread("imgs/TopLeftCorner.png")
top_left_gray = cv2.cvtColor(top_left, cv2.COLOR_RGB2GRAY)
top_left_w, top_left_h = top_left_gray.shape[::-1]
lower_right = cv2.imread("imgs/LowerRightCorner.png")
lower_right_gray = cv2.cvtColor(lower_right, cv2.COLOR_RGB2GRAY)
lower_right_w, lower_right_h = lower_right_gray.shape[::-1]

# game window dimensions
x, y, w, h = None, None, None, None

# wait
sleep(3)

# main
loop_time = time()
while True:
    # Check if the location of the pitch is found
    if x and y and w and h:
        # screenshot
        screenshot = pyautogui.screenshot(region=(x, y, w, h))
        image = np.array(screenshot)
        # Convert RGB to BGR
        image = image[:, :, ::-1].copy()
        image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        # Find noses
        result = cv2.matchTemplate(image_gray, template_gray, method)
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), template_w, template_h]
            rectangles.append(rect)
            rectangles.append(rect)
        # Remove duplicates in rectangles
        rectangles, _ = cv2.groupRectangles(rectangles, eps=0.5, groupThreshold=1)
        # Click on all detected noses
        for (rx, ry, rw, rh) in rectangles:
            center_x = rx + int(rw / 2)
            center_y = ry + int(rh / 2)
            pyautogui.click(x=x + center_x, y=y + center_y)
        print("FPS {}".format(1 / (time() - loop_time)))
        loop_time = time()
    else:
        # Find upper left and lower right corner
        upper_left_location = pyautogui.locateOnScreen(
            "imgs/TopLeftCorner.png", confidence=0.9
        )
        lower_right_location = pyautogui.locateOnScreen(
            "imgs/LowerRightCorner.png", confidence=0.9
        )
        if upper_left_location and lower_right_location:
            x = upper_left_location.left
            y = upper_left_location.top
            w = lower_right_location.left - upper_left_location.left
            h = (
                lower_right_location.top
                + lower_right_location.height
                - upper_left_location.top
            )
