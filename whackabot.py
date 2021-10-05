# https://www.classicgame.com/game/Whack+a+Mole

# imports
import cv2
import pyautogui
from time import sleep, time
import numpy as np

# No cooldown time
pyautogui.PAUSE = 0
method = cv2.TM_CCOEFF_NORMED

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
    if x and y and w and h:
        # screenshot
        screenshot = pyautogui.screenshot(region=(x, y, w, h))
        image = np.array(screenshot)
        # Convert RGB to BGR
        image = image[:, :, ::-1].copy()

        while True:

            # show what the computer sees
            image_mini = cv2.resize(
                src=image, dsize=(450, 350)  # must be integer, not float
            )
            cv2.imshow("vision", image_mini)
            cv2.waitKey(10)

            image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

            result = cv2.matchTemplate(
                image=image_gray, templ=template_gray, method=method
            )

            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            # threshold
            if max_val >= 0.8:
                pyautogui.click(x=max_loc[0] + x, y=max_loc[1] + y)

                image = cv2.rectangle(
                    img=image,
                    pt1=max_loc,
                    pt2=(
                        max_loc[0] + template_w,  # = pt2 x
                        max_loc[1] + template_h,  # = pt2 y
                    ),
                    color=(0, 0, 255),
                    thickness=-1,  # fill the rectangle
                )

            else:
                break
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
