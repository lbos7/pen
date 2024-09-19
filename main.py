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
    grey_color = 250
    bg_removed = cam.get_color_image(frames)
    depth_colormap = cam.get_depth_colormap(frames)
    bg_removed_blurred = cv2.bilateralFilter(bg_removed, 5, 150, 150)
    # bg_removed_blurred = cv2.blur(bg_removed, (5, 5))
    # images = np.hstack((bg_removed, depth_colormap))
    # upper_hsv = np.array([cv2.getTrackbarPos('H High', 'Main'), cv2.getTrackbarPos('S High', 'Main'), cv2.getTrackbarPos('V High', 'Main')])
    # lower_hsv = np.array([cv2.getTrackbarPos('H Low', 'Main'), cv2.getTrackbarPos('S Low', 'Main'), cv2.getTrackbarPos('V Low', 'Main')])
    upper_hsv = np.array([156, 255, 255])
    lower_hsv = np.array([116, 76, 0])
    mask = cam.adjust_mask(bg_removed_blurred, upper_hsv, lower_hsv)
    masked_image = cv2.bitwise_and(bg_removed_blurred, bg_removed_blurred, mask=mask)
    masked_image_gray = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(masked_image_gray, 10, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    largest_area = 0
    where = 0
    cx = 0
    cy = 0
    if len(contours) != 0:
        c = max(contours, key = cv2.contourArea)
        M = cv2.moments(c)
        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
    cv2.drawContours(bg_removed, contours, -1, (0, 255, 0), 1)
    cv2.circle(bg_removed, (cx, cy), 2, (0, 0, 255), 2)
    cv2.imshow('Main', np.hstack((bg_removed, masked_image)))
    key = cv2.waitKey(1)
    # Press esc or 'q' to close the image window
    if key & 0xFF == ord('q') or key == 27:
        cv2.destroyAllWindows()
        break
cam.stop_pipeline()