import serial
import time
# from buildhat import Hat
# hat = Hat()

#time.sleep(30)

ser = serial.Serial ("/dev/serial0", 115200)

time.sleep(1)
#ser.write(f'port 2 ; list\r'.encode())
ser.write(f'port 2 ; plimit 1 ; bias .4; pwm; set 0.4\r'.encode())
print('it is written')  #Open port with baud rate


# start_time = time.time()

# while True:
#   current_time = time.time()
#   if current_time - start_time >5:
#     break
#   received_data = ser.readline()              #read serial port
#   print(received_data)
#   time.sleep(0.01)

time.sleep(2)
  
ser.write(f'set 0\r'.encode())               #print received data
       