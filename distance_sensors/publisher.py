import zmq

from SensorGroup import SensorGroup
from DistanceSensor import DistanceSensor
import RPi.GPIO as GPIO

context = zmq.Context()
ipc_socket = context.socket(zmq.PUB)
ipc_socket.bind("ipc://distance")


GPIO.setmode(GPIO.BCM)

r1 = DistanceSensor(21,20,'r1')
r2 = DistanceSensor(26,19,'r2')

sensorGroup = SensorGroup(sensors=[r1])


try:
  for reading in sensorGroup.measure():
    print(reading)
    ipc_socket.send_pyobj(reading)
except KeyboardInterrupt:
    GPIO.cleanup()
except:  
    # this catches ALL other exceptions including errors.  
    # You won't get any error messages for debugging  
    # so only use it once your code is working  
    print("Other error or exception occurred!")  
  
finally:  
    GPIO.cleanup() # this ensures a clean exit  

# try:
#   while True:
#     reading = sensorGroup.measure()
#     ipc_socket.send_pyobj(reading)
# except KeyboardInterrupt:
#     GPIO.cleanup()
# except:  
#     # this catches ALL other exceptions including errors.  
#     # You won't get any error messages for debugging  
#     # so only use it once your code is working  
#     print("Other error or exception occurred!")  
  
# finally:  
#     GPIO.cleanup() # this ensures a clean exit  
