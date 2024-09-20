from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
from interbotix_common_modules.common_robot.robot import robot_shutdown, robot_startup
from math import pi
import modern_robotics as mr
import numpy as np

class Robot:

    def __init__(self, robot:InterbotixManipulatorXS):
        self.robot = robot

    def start_running(self):
        robot_startup()

    def stop_running(self):
        robot_shutdown()

    def move_ee_pos_cart_abs(self, x, y, z):
        self.robot.arm.set_ee_pose_components(x, y, z)

    def move_ee_pos_cyl_abs(self, r, theta, z):
        x = r*np.cos(np.radians(theta))
        y = r*np.sin(np.radians(theta))
        self.robot.arm.set_ee_pose_components(x, y, z)

    def home_pos(self):
        self.robot.arm.go_to_home_pose()

    def sleep_pos(self):
        self.robot.arm.go_to_sleep_pose()

    def grab(self):
        self.robot.gripper.grasp()

    def release(self):
        self.robot.gripper.release()

    def get_ee_pos_cart(self):
        pose_mat = self.robot.arm.get_ee_pose()
        return [pose_mat[0][-1], pose_mat[1][-1], pose_mat[2][-1]]
    
    def get_ee_pos_cyl(self):
        pose_mat = self.robot.arm.get_ee_pose()
        r = np.sqrt(pose_mat[0][-1]**2 + pose_mat[1][-1]**2)
        theta = np.arctan2(pose_mat[1][-1], pose_mat[0][-1])
        return [r, np.degrees(theta), pose_mat[2][-1]]
    
    

    
