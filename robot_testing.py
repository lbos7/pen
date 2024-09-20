from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
from interbotix_common_modules.common_robot.robot import robot_shutdown, robot_startup
from math import pi
# The robot object is what you use to control the robot
robot = InterbotixManipulatorXS("px100", "arm", "gripper")

robot_startup()
mode = 'h'
print(robot.arm.group_info.joint_names)
# Let the user select the position
while mode != 'q':
    mode=input("[h]ome, [s]leep, [go] - open gripper, [gc] - close gripper, [wccw] - waist counter-clockwise, [wcw] - waist clockwise, [shu] - shoulder up,\n[shd] - shoulder down, [eu] - elbow up, [ed] - elbow down, [q]uit ")
    if mode == "h":
        robot.arm.go_to_home_pose()
    elif mode == "s":
        robot.arm.go_to_sleep_pose()
    elif mode == "gc":
        robot.gripper.grasp()
    elif mode == "go":
        robot.gripper.release()
    elif mode == "wccw":
        robot.arm.set_single_joint_position('waist', pi/6)
    elif mode == "wcw":
        robot.arm.set_single_joint_position('waist', -pi/6)
    elif mode == "shd":
        robot.arm.set_single_joint_position('shoulder', pi/6)
    elif mode == "shu":
        robot.arm.set_single_joint_position('shoulder', -pi/6)
    elif mode == "ed":
        robot.arm.set_single_joint_position('elbow', pi/6)
    elif mode == "eu":
        robot.arm.set_single_joint_position('elbow', -pi/6)


robot_shutdown()