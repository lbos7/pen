from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
from robot import Robot
from math import pi
# The robot object is what you use to control the robot
interbotix_robot = InterbotixManipulatorXS("px100", "arm", "gripper")
robot = Robot(interbotix_robot)

robot.start_running()
mode = 'h'
# Let the user select the position
while mode != 'q':
    mode=input("[h]ome, [s]leep, [go] - open gripper, [gc] - close gripper, [wccw] - waist counter-clockwise, [wcw] - waist clockwise, [shu] - shoulder up,\n[shd] - shoulder down, [eu] - elbow up, [ed] - elbow down, [pos] - display position, [r,theta,z] - move to position in cylindrical cords [q]uit ")
    if mode == "h":
        robot.home_pos()
    elif mode == "s":
        robot.sleep_pos()
    elif mode == "gc":
        robot.grab()
    elif mode == "go":
        robot.release()
    elif mode == "wccw":
        robot.robot.arm.set_single_joint_position('waist', pi/6)
    elif mode == "wcw":
        robot.robot.arm.set_single_joint_position('waist', -pi/6)
    elif mode == "shd":
        robot.robot.arm.set_single_joint_position('shoulder', pi/6)
    elif mode == "shu":
        robot.robot.arm.set_single_joint_position('shoulder', -pi/6)
    elif mode == "ed":
        robot.robot.arm.set_single_joint_position('elbow', pi/6)
    elif mode == "eu":
        robot.robot.arm.set_single_joint_position('elbow', -pi/6)
    elif mode == "pos":
        print(robot.get_ee_pos_cart())
        print(robot.get_ee_pos_cyl())
    elif "," in mode:
        cords = mode.split(",")
        robot.move_ee_pos_cyl_abs(float(cords[0]), float(cords[1]), float(cords[2]))


robot.stop_running()