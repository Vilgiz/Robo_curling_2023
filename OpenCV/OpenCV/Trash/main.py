import time
from Robot import Robot

robot = Robot(timeout=10, print_debug=True)
robot.start()

while True:
    robot.send_step([1, 1], 1)
    time.sleep(2)