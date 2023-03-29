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
        self.set_point = 25 #cm
        #good results with 
        #self.controller = PIController(proportional_constant=0.4,integral_constant=0,derivative_constant=0.05)
        #turns a bit quick though if starts not on set point so going to try weakening response a bit
        self.controller = PIController(proportional_constant=0.8,integral_constant=0.014,derivative_constant=0)
        self.previous = None
        self.current = None
        self.forward_speed = 30

    def updateDistance(self,distance):
     
     self.previous = self.current
     self.current = distance
    
    
    async def update(self,distance): 
      # #await asyncio.sleep(0.00001)
      #print(distance)
      
      self.updateDistance(distance)
      
      
      if(self.current>=100.0 and (not self.previous>=100)):
        return
      if(not self.previous):
          left_speed = 0
          right_speed = 0
      else:
        y=(1)*(distance - self.set_point) #+ve if on left side of set point line
        l = 0*(distance-self.previous)  #+ve if pointing away from wall/furhter to left
        error = y
        print('error',error)
        adjustment = self.controller.get_value(error)
        print(adjustment)
        left_speed = self.forward_speed+adjustment
        right_speed = self.forward_speed - adjustment
        self.left_motor.pwm(left_speed)
        self.right_motor.pwm(right_speed)

    def start(self):
       print('asdfsadfsadfsadfsadfsdfsadf')
       self.distance_emitter.add_listener('r1',self.update)

    def stop(self):
       self.distance_emitter.remove_listener('r1',self.update)
       self.left_motor.pwm(0)
       self.right_motor.pwm(0)

