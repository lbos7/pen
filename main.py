from camera import Camera
import numpy as np
import cv2

cam = Camera()

while True:
    frames = cam.get_frames()
    grey_color = 153
    bg_removed = cam.remove_background(frames, 1, grey_color)
    depth_colormap = cam.get_depth_colormap(frames)
    images = np.hstack((bg_removed, depth_colormap))
    cv2.imshow('Main', bg_removed)
    key = cv2.waitKey(1)
    # Press esc or 'q' to close the image window
    if key & 0xFF == ord('q') or key == 27:
        cv2.destroyAllWindows()
        break
cam.stop_pipeline()