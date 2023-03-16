from Motors.Motor import Motor
from Motors.MotorProtocol import MotorProtocol
import serial_asyncio
import asyncio


async def configure():
    loop = asyncio.get_event_loop()
    transport,protocol = await serial_asyncio.create_serial_connection(loop, MotorProtocol, "/dev/serial0", baudrate=115200)
    left_motor = Motor('C',transport,-1)
    right_motor = Motor('D',transport)
    protocol.motors.append(left_motor)
    protocol.motors.append(right_motor)
    return (left_motor,right_motor)

