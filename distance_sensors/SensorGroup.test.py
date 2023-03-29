from SensorGroup import SensorGroup
from DistanceSensor import DistanceSensor
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)


r1 = DistanceSensor(21,20,'r1')
r2 = DistanceSensor(26,19,'r2')

sensorGroup = SensorGroup(sensors=[r1,r2],delay_between_pings_ms =1*1000)



try:
  while True:
    reading = sensorGroup.measure()
    print(reading)
except KeyboardInterrupt:
    GPIO.cleanup()
except:  
    # this catches ALL other exceptions including errors.  
    # You won't get any error messages for debugging  
    # so only use it once your code is working  
    print("Other error or exception occurred!")  
  
finally:  
    GPIO.cleanup() # this ensures a clean exit  