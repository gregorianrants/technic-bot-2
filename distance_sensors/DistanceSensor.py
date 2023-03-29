import RPi.GPIO as GPIO
import time

START_LOW = 'START_LOW'
GONE_HIGH = 'GONE_HIGH'
END_LOW = 'END_LOW'

class DistanceSensor:
    def __init__(self,trig_pin,echo_pin,name):
        self.name = name
        self.trigPin = trig_pin
        self.echoPin = echo_pin
        GPIO.setup(self.trigPin,GPIO.OUT)
        GPIO.setup(self.echoPin,GPIO.IN)
        self.setTrigLow()

    def reset(self):
        self.setTrigLow()
        
    def setTrigLow(self):
        GPIO.output(self.trigPin,0)

    def setTrigHigh(self):
         GPIO.output(self.trigPin,1)

    def echoIsLow(self):
        return GPIO.input(self.echoPin)==0
    
    def echoIsHigh(self):
        return GPIO.input(self.echoPin)==1
    
    def update_start_low(self):
        if self.echoIsHigh():
            print('hello')
            self.state = GONE_HIGH
            self.echo_start_time = time.time()
    
    def update_gone_high(self):
        if self.echoIsLow():
            self.state = END_LOW
            self.echo_end_time = time.time()

    def get_distance(self,echo_end_time,echo_start_time):
        travel_time = echo_end_time-echo_start_time
        meters = (travel_time/2)*343
        cm = round(meters*100,2)
        return cm


    def update(self):
        if(self.state==START_LOW): self.update_start_low()
        if(self.state==GONE_HIGH): self.update_gone_high()

    def getReading(self):
        echoStartTime = None
        echoStopTime = None
        trigSendTime = None
        self.setTrigLow()
        time.sleep(2E-6)
        self.setTrigHigh()
        time.sleep(10E-6)
        self.setTrigLow()
        trigSendTime = time.time()
        while self.echoIsLow():
            pass
        echoStartTime=time.time()
        while self.echoIsHigh():
            pass
        echoStopTime=time.time()
        distance_cm = self.get_distance(echoStopTime,echoStartTime)
        return distance_cm



