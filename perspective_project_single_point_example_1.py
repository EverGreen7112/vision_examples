import copy
import math
import numpy as np
import cv2

WIDTH = 1280
HEIGHT = 720
WINDOW_NAME = "window"
SPEED = 0.5  # the speed we want the point to move at (units/milisec)
MIN_Z = 50  # we cant have z = 0 as we will end up with division by 0
POINT_COLOR = (255, 0, 0)  # the color of the point as rendered (BGR)
POINT_RADIUS = 10  # the radius of the point as rendered (pixels)
FOV_X = math.radians(61)
FOV_Y = math.radians(37)

# calculating the focal length from the FOV
F_LENGTH_X = WIDTH / (2 * math.tan(FOV_X / 2))
F_LENGTH_Y = HEIGHT / (2 * math.tan(FOV_Y / 2))

# these are the values that will change at runtime
position = [0, 0, MIN_Z]
run = True


def handle_input(key: int):
    global run, position, SPEED
    if key == ord('w'):
        position[1] -= SPEED
    elif key == ord('s'):
        position[1] += SPEED
    elif key == ord('a'):
        position[0] -= SPEED
    elif key == ord('d'):
        position[0] += SPEED
    elif key == ord(' '):
        position[2] += SPEED
    elif key == 8:  # backspace
        position[2] = max(position[2] - SPEED, MIN_Z)
    elif key == 27:  # esc
        run = False


def perspective_project_point(point: list[float, float, float],
                              focal_length_x: float,
                              focal_length_y: float,
                              width_pixels: int,
                              height_pixels: int) -> np.ndarray[float, float]:
    projected = np.array([point[0] * focal_length_x, point[1] * focal_length_y])
    projected /= point[2]
    projected += (np.array([width_pixels, height_pixels]) / 2)
    return projected


def main():
    blank = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)  # creates an empty black image
    while run:
        img = copy.copy(blank)
        projected = perspective_project_point(position,
                                              F_LENGTH_X,
                                              F_LENGTH_Y,
                                              WIDTH,
                                              HEIGHT)
        cv2.circle(img,
                   (int(projected[0]), int(projected[1])),  # must cast to an int as we cant have a non whole pixel pos
                   int(POINT_RADIUS * 0.5),  # this calculation is to compensate for the lines width
                   POINT_COLOR,
                   POINT_RADIUS  # the width is equal to the radius so the circle will be full
                   )
        cv2.imshow(WINDOW_NAME, img)
        key = cv2.waitKey(1)
        handle_input(key)


if __name__ == '__main__':
    main()
