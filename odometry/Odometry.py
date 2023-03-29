import math
import asyncio




class Odometry:
    def __init__(self,leftMotor,rightMotor):
        self.x = 0
        self.y = 0
        self.theta = math.pi/2
        self.leftMotor = leftMotor
        self.rightMotor = rightMotor

    async def start(self):
        while True:
            await asyncio.sleep(0.2)
            print(self.leftMotor.getPosition())
