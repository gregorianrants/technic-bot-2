from Motors.configure_motors import configure
from atomic_behaviours.MotorSpeed import MotorSpeed
import asyncio,signal
import time

# left_encoder = Encoder(motors.left_motor,'left',log_data='test')
# right_encoder = Encoder(motors.right_motor,'right')

def find_V_R(V_L,R_L,w):
    return (V_L * (R_L+w))/R_L

V_L = 20
V_R = find_V_R(V_L,200,176)

print(V_R)




async def main():
        left_motor,right_motor = await configure()
        left_motor.start_data_stream()
        right_motor.start_data_stream()
        left_motor_speed = MotorSpeed(left_motor,V_L)
        right_motor_speed = MotorSpeed(right_motor,V_R)
        right_motor_speed.start()
        left_motor_speed.start()

        def shutdown():
                left_motor_speed.stop()
                right_motor_speed.stop()
                tasks = asyncio.all_tasks()
                [task.cancel() for task in tasks]
                left_motor.pwm(0)
                right_motor.pwm(0)
                

        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGINT,shutdown)
        await asyncio.sleep(10)
        left_motor_speed.stop()
        right_motor_speed.stop()
        #left_motor.add_listener('encoder',print_encoder_data)
        #right_motor.add_listener('encoder',print_encoder_data)
        await asyncio.sleep(2)
        left_motor.pwm(0)
        right_motor.pwm(0)

        
        left_motor_speed.stop()
        right_motor_speed.stop()
        left_motor.pwm(0)
        right_motor.pwm(0)



loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()






