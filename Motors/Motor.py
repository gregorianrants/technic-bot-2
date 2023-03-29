from event_emitter_asyncio.EventEmitter import EventEmitter
import asyncio

class PositionEncoder:
    def __init__(self,motor):
      self.previous_read = None
      self.most_recent_value = None
      self.update = self.initial_update
      self.motor = motor


    def initial_update(self,encoder_data):
      _,_,encoder_pos_in_mm,_,timestamp = encoder_data
      self.previous_read = encoder_pos_in_mm
      print(self.previous_read)
      self.most_recent_value = encoder_pos_in_mm
      self.update = self.subsequent_updates

    def subsequent_updates(self,encoder_data):
      _,_,encoder_pos_in_mm,_,timestamp = encoder_data
      self.most_recent_value = encoder_pos_in_mm

    def read(self):
       if(self.most_recent_value==None or self.previous_read==None):
          return 0
       result = self.most_recent_value - self.previous_read
       self.previous_read = self.most_recent_value
       return result
       
    def start(self):
       self.motor.add_listener('encoder',self.update)   
    



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
        self.position_encoder = PositionEncoder(self)
        self.position_encoder.start()

    def getPosition(self):
       return self.position_encoder.read()

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
    
    def getDistance(self,pos):
         distance = pos/360*self.wheel_diameter
         return distance

    def data_handler(self,line,line_timestamp):
       if(line[:5]==f'P{self.port_index}C0:'):
            data_array_as_strings = line.split()[1:]
            try: 
              speed,pos,apos = [int(data_string) for data_string in data_array_as_strings]
            except ValueError:
               self.pwm(0)
               loop = asyncio.get_event_loop()
               loop.close()
               
               
            speed = self.getSpeed(speed)
            self.emit('encoder',[
                self.port_letter,
                self.direction*speed,
                self.direction*self.getDistance(pos),
                self.direction*apos,
                line_timestamp])

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

    
    def start_data_stream_both(self):
      self.transport.write(f'port {2}; select 0; selrate 10;port {3}; select 0; selrate 10\r'.encode())
       
       


