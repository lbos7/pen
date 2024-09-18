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
    

    def stop_pipeline(self):
        self.pipeline

