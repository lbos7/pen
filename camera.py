import pyrealsense2 as rs
import numpy as np
import cv2

class Camera:

    def __init__(self):
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        self.profile = self.pipeline.start(self.config)
        self.align = rs.align(rs.stream.color)
        self.depth_scale = self.profile.get_device().first_depth_sensor().get_depth_scale()


    def get_frames(self):
        frames = self.pipeline.wait_for_frames()
        return self.align.process(frames)
    
    def remove_background(self, frames, dist, color):
        depth_image = np.asanyarray(frames.get_depth_frame().get_data())
        color_image = np.asanyarray(frames.get_color_frame().get_data())
        depth_image_3d = np.dstack((depth_image, depth_image, depth_image))
        return np.where((depth_image_3d > dist/self.depth_scale) | (depth_image_3d <= 0), color, color_image)
    
    def get_depth_colormap(self, frames):
        depth_image = np.asanyarray(frames.get_depth_frame().get_data())
        return cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
    
    def get_depth_image(self, frames):
        return np.asanyarray(frames.get_depth_frame().get_data())
    
    def get_color_image(self, frames):
        return np.asanyarray(frames.get_color_frame().get_data())
    
    def adjust_mask(self, image, upper_hsv, lower_hsv):
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        return cv2.inRange(hsv_image, lower_hsv, upper_hsv)
    
    def get_contours(self, frames):
        color_image = self.get_color_image(frames)
        blurred = cv2.bilateralFilter(color_image, 5, 150, 150)
        upper_hsv = np.array([156, 255, 255])
        lower_hsv = np.array([116, 76, 0])
        mask = self.adjust_mask(blurred, upper_hsv, lower_hsv)
        masked_image = cv2.bitwise_and(blurred, blurred, mask=mask)
        masked_image_gray = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(masked_image_gray, 10, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours
    
    def get_point_pos(self, frames, contours):
        cx = 0
        cy = 0
        if len(contours) != 0:
            c = max(contours, key = cv2.contourArea)
            M = cv2.moments(c)
            if M['m00'] != 0:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
        return [cx, cy, self.depth_scale*self.get_depth_image(frames)[cy][cx]]

    def stop_pipeline(self):
        self.pipeline

