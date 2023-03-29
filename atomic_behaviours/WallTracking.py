print(__name__)

import asyncio

from distance_sensors.distance_emitter import distance_emitter 
from utilities.pid_controller import PIController
import time


class WallTracking:
    def __init__(self,left_motor,right_motor):
        self.distance_emitter = distance_emitter
        self.left_motor = left_motor
        self.right_motor = right_motor
        #time.sleep(1)
        self.set_point = 20 #cm
        #good results with 
        #self.controller = PIController(proportional_constant=0.4,integral_constant=0,derivative_constant=0.05)
        #turns a bit quick though if starts not on set point so going to try weakening response a bit
        self.controller = PIController(proportional_constant=0.3,integral_constant=0.002,derivative_constant=0.05)
        self.previous_r1 = None
        self.current_r1 = None
        self.previous_r2 = None
        self.current_r1 = None
        self.forward_speed = 30

    def updateDistances(self,r1,r2):
     self.previous_r1 = self.current_r1
     self.current_r1 = r1
     self.previous_r2 = self.current_r1
     self.current_r2 = r1
    
    async def update(self,distances): 
      #await asyncio.sleep(0.00001)
      r1 = distances['r1']
      r2 = distances['r2']+4.7
      self.updateDistances(r1,r2)
      
      
      if(self.current_r1==100.0 and self.previous_r1!=100):
        return
      if(not self.previous_r1):
          left_speed = self.forward_speed
          right_speed = self.forward_speed
      else:
        y=r1 - self.set_point #+ve if on left side of set point line
        l = r1-r2  #+ve if pointing away from wall/furhter to left
        error = l+y
        print('error',error)
        adjustment = self.controller.get_value(error)
        left_speed = self.forward_speed+adjustment
        right_speed = self.forward_speed - adjustment
      self.left_motor.pwm(left_speed)
      self.right_motor.pwm(right_speed)

    def start(self):
       print('asdfsadfsadfsadfsadfsdfsadf')
       self.distance_emitter.add_listener('distance',self.update)

    def stop(self):
       self.distance_emitter.remove_listener('distance',self.update)
       self.left_motor.pwm(0)
       self.right_motor.pwm(0)

