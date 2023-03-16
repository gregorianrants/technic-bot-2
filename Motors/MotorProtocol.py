import asyncio

class MotorProtocol(asyncio.Protocol):
    def __init__(self):
        self.buffer = bytearray(b'')
        self.handler = self.setup_handler
        self.loading_bootloader = False
        #TODO add a method for adding and removing motors and make sure we dont get duplicates
        self.motors = []

    def connection_made(self, transport):
        self.transport = transport
        print('port opened', transport)
        transport.serial.rts = False  # You can manipulate Serial object via transport
        transport.write(b'version\r')
       

    def setup_handler(self,line):
        #print(line)
        if('BuildHAT bootloader version' in line):
            raise Exception('the firmware needs loaded each time pi is restarted run load firmware script then restart')

        if('Firmware version' in line):
            print('i handled it')
            self.handler = self.running_handler
            #self.transport.write(f'port 3 ; plimit 1 ; bias .4; pwm; set 0.4; select 0\r'.encode())

    #todo consider getting rid of and by changing the function which is run once there is a motor c
    def running_handler(self,line):
        for motor in self.motors:
            motor.data_handler(line)

    def data_received(self, data):
        for byte_as_int in data:
            if byte_as_int==10:
                self.handler(self.buffer.decode())
                self.buffer = bytearray(b'')
            else: 
                self.buffer.append(byte_as_int)
        pass
       
    def connection_lost(self, exc):
        #print('port closed')
        #self.transport.loop.stop()
        pass