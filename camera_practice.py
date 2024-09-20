from camera import Camera
import numpy as np
import cv2

def f(x):
    pass

cam = Camera()

cv2.namedWindow('Main', cv2.WINDOW_NORMAL)
cv2.createTrackbar('H High','Main',179,179, lambda x:x)
cv2.createTrackbar('H Low','Main',0,179, lambda x:x)
cv2.createTrackbar('S High','Main',255,255, lambda x:x)
cv2.createTrackbar('S Low','Main',0,255, lambda x:x)
cv2.createTrackbar('V High','Main',255,255, lambda x:x)
cv2.createTrackbar('V Low','Main',0,255, lambda x:x)

while True:
    frames = cam.get_frames()
    color_image = cam.get_color_image(frames)
    contours = cam.get_contours(frames)
    centroid_pos = cam.get_point_pos(frames, contours)
    # cv2.drawContours(bg_removed, contours, -1, (0, 255, 0), 1)
    cv2.circle(color_image, (centroid_pos[0], centroid_pos[1]), 2, (0, 0, 255), 2)
    cv2.imshow('Main', color_image)
    key = cv2.waitKey(1)
    # Press esc or 'q' to close the image window
    if key & 0xFF == ord('q') or key == 27:
        cv2.destroyAllWindows()
        break

cam.stop_pipeline()