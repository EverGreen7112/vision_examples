import copy
import math
import numpy as np
import cv2

WIDTH = 1280
HEIGHT = 720
WINDOW_NAME = "window"
SPEED = 0.5  # the speed we want the camera to move at (units/milisec)
ANGULAR_SPEED = math.radians(0.8)  # the speed we want the camera to turn at (rad/milisec)
POINT_COLOR = (255, 0, 0)  # the color of the points as rendered (BGR)
LINE_COLOR = (0, 255, 0)  # the color of the lines as rendered (BGR)
POINT_RADIUS = 10  # the radius of a point as rendered (pixels)
LINE_WIDTH = 3  # the width of the lines as rendered (pixels)
FOV_X = math.radians(61)
FOV_Y = math.radians(37)
SHAPE = np.array([
    [1,  1,  -1,  -1, -1,  -1,  1,  1],
    [1,  -1,  -1,  1, 1,  -1,  -1,  1],
    [50,  50, 50, 50, 48, 48,  48, 48],
    [1,   1,  1,   1, 1,   1,   1,  1]
])
# calculating the focal length from the FOV
F_LENGTH_X = WIDTH / (2 * math.tan(FOV_X / 2))
F_LENGTH_Y = HEIGHT / (2 * math.tan(FOV_Y / 2))

INTRINSIC_MATRIX = np.array([
     [F_LENGTH_X, 0,          WIDTH / 2,  0],
     [0,          F_LENGTH_Y, HEIGHT / 2, 0],
     [0,          0,          1,          0]
                            ])
# these are the values that will change at runtime
position = [0, 0, 0]
rotation = [0, 0, 0]
run = True


def rotation_matrix_affine_yaw_pitch_roll(yaw=0.0, pitch=0.0, roll=0.0) -> np.ndarray:
    c1 = np.cos(pitch)
    s1 = np.sin(pitch)
    c2 = np.cos(yaw)
    s2 = np.sin(yaw)
    c3 = np.cos(roll)
    s3 = np.sin(roll)
    return np.array([[c2 * c3, -c2 * s3, s2, 0],
                     [c1 * s3 + c3 * s1 * s2, c1 * c3 - s1 * s2 * s3, -c2 * s1, 0],
                     [s1 * s3 - c1 * c3 * s2, c3 * s1 + c1 * s2 * s3, c1 * c2, 0],
                     [0, 0, 0, 1]])


def handle_input(key: int):
    global run, position, SPEED
    if key == ord('w'):
        position[2] -= SPEED
    elif key == ord('s'):
        position[2] += SPEED
    elif key == ord('a'):
        position[0] += SPEED
    elif key == ord('d'):
        position[0] -= SPEED
    elif key == ord(' '):
        position[1] += SPEED
    elif key == 8:  # backspace
        position[1] -= SPEED
    elif key == ord('q'):
        rotation[0] -= ANGULAR_SPEED
    elif key == ord('e'):
        rotation[0] += ANGULAR_SPEED
    elif key == 27:  # esc
        run = False


def main():
    blank = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)  # creates an empty black image
    while run:
        img = copy.copy(blank)

        #  the extrinsic matrix is the rotation matrix @ translation matrix
        extrinsic_matrix = rotation_matrix_affine_yaw_pitch_roll(*rotation) @ np.array([
            [1, 0, 0, position[0]],
            [0, 1, 0, position[1]],
            [0, 0, 1, position[2]],
            [0, 0, 0,           1]
        ])
        projection_matrix = INTRINSIC_MATRIX @ extrinsic_matrix
        projected_shape = projection_matrix @ SHAPE
        points_positions = np.transpose(projected_shape)  # we transpose the matrix to make it a list of vectors

        # these are the projected positions of the shape's points in the frame
        points_frame = [(int(point[0] / point[2]), int(point[1] / point[2])) for point in points_positions]

        # draw lines
        for i in range(len(points_frame)):
            point = points_frame[i]
            next_point = points_frame[(i+1) % len(points_frame)]
            cv2.line(img, point, next_point, LINE_COLOR, LINE_WIDTH)

        # draw points
        for point in points_frame:
            cv2.circle(img,
                       point,
                       int(POINT_RADIUS * 0.5),  # this calculation is to compensate for the lines width
                       POINT_COLOR,
                       POINT_RADIUS  # the width is equal to the radius so the circle will be full
                       )
        cv2.imshow(WINDOW_NAME, img)
        key = cv2.waitKey(1)

        print(key)
        handle_input(key)


if __name__ == '__main__':
    main()
