from Motors.configure_motors import configure
from distance_sensors.distance_emitter import distance_emitter 
from atomic_behaviours.WallTracking import WallTracking
import asyncio,signal


async def main():
    left_motor,right_motor = await configure()
    wall_follower = WallTracking(left_motor,right_motor)
    wall_follower.start()
    left_motor.start_data_stream()
    right_motor.start_data_stream()

    def shutdown():
                wall_follower.stop()
                tasks = asyncio.all_tasks()
                [task.cancel() for task in tasks]
                left_motor.pwm(0)
                right_motor.pwm(0)
                

    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT,shutdown)
    distance_task = asyncio.create_task(distance_emitter.start())
    await distance_task


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('stopiing')
finally:
    print('finally')