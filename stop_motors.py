from buildhat import Motor
import time

left = Motor('C')
right = Motor('D')

time.sleep(30)

def handle_rotation(value1,value2,value3):
    print(value1,value2,value3)

left.when_rotated = handle_rotation


left.stop()
right.stop()