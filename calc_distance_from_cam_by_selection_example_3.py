import cv2
import math

cap = cv2.VideoCapture(0)

WIDTH = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
HEIGHT = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# these values are for lifecam 3000 hd camera
F_LENGTH_X_LIFECAM = (1 / (math.tan(0.5355780593748425) * 2)) * WIDTH
F_LENGTH_Y_LIFECAM = (1 / (math.tan(0.3221767906849529) * 2)) * HEIGHT

OBJECT_WIDTH = 15
OBJECT_HEIGHT = 15

def main():
    key = cv2.waitKey(1)
    while key != ord('q'):
        ok, frame = cap.read()
        cv2.imshow('feed', frame)
        key = cv2.waitKey(1)
        if (key == ord('s')) and ok:
            bbox = cv2.selectROI('feed', frame)
            # bbox[0] is x in frame (selection's top left)
            # bbox[1] is y in frame (selection's top left)
            # bbox[2] is width in frame
            # bbox[3] is height in frame

            # this is the surface of the object IRL
            object_surface = OBJECT_HEIGHT*OBJECT_WIDTH
            # this is the surface of the object in frame
            object_surface_frame = bbox[2]*bbox[3]

            surface_to_frame_ratio = object_surface/object_surface_frame
            z = (surface_to_frame_ratio*(F_LENGTH_Y_LIFECAM*F_LENGTH_X_LIFECAM))**0.5

            # the location of the objects center in frame if the frames center is the (0,0) point
            x_frame = bbox[0] - (WIDTH * 0.5) + (bbox[2] * 0.5)
            y_frame = bbox[1] - (HEIGHT * 0.5) + (bbox[3] * 0.5)

            x = (x_frame * z) / F_LENGTH_X_LIFECAM
            y = (y_frame * z) / F_LENGTH_Y_LIFECAM

            print((x, y, z))


if __name__ == '__main__':
    main()
