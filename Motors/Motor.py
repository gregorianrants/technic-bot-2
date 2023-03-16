from event_emitter_asyncio.EventEmitter import EventEmitter

class Motor(EventEmitter):
    def __init__(self,port,transport,direction=1):
        super().__init__()
        port_letters = ['A','B','C','D']
        self.port_letter = port
        self.direction = direction
        try:
          self.port_index = port_letters.index(port)
        except ValueError:
          print(f'{port} is not a valid port')

        self.transport = transport
        self.wheel_diameter = 276 #mm

    def write(self,data):
       self.transport.write(f'port {self.port_index}; {data}\r'.encode())
       
    def set_bias(self,bias=0.4):
        data = f'bias {bias}'
        self.transport.write(data)

    def set_plimit(self,plimit=1):
        data = f'plimit {plimit}'
        self.transport.write(data)

    def getSpeed(self,aSpeed):
         speed =  (aSpeed/360)*self.wheel_diameter
         return speed

    def data_handler(self,line):
       if(line[:5]==f'P{self.port_index}C0:'):
            data_array_as_strings = line.split()[1:]
            speed,pos,apos = [int(data_string) for data_string in data_array_as_strings]
            speed = self.getSpeed(speed)
            self.emit('encoder',[self.port_letter,self.direction*speed,self.direction*pos,self.direction*apos])

    #todo consider setting pwm on init
    def pwm(self,pwm):
       pwm = (pwm * self.direction)/100
       if(pwm>1 or pwm<-1):
          raise ValueError('pwm must be between -1 and 1')
       data = f'pwm; set {pwm};'
       self.write(data)

    def start_data_stream(self):
       data = f'select 0; selrate 10'
       self.write(data)
       


