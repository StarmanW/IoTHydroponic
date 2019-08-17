import time
import serial
import asyncio
from servo import Servo
from firebase import Firebase

# Servo pin declaration
feed_servo = Servo(18)
pH_servo = Servo(22)

# Change ACM number as found from "ls /dev/tty/ACM*"
ser = serial.Serial("/dev/ttyACM0",9600)
ser.baudrate=9600

# Setup firebase
firebase = Firebase('./firebase.json')
firebase.run()

'''
    Async function to perform fish
    feeding at an interval
'''
async def periodic():
    while True:
        pwm_feed_servo.ChangeDutyCycle(MIN_DUTY)
        await asyncio.sleep(0.5)
        pwm_feed_servo.ChangeDutyCycle(CENTRE)
        await asyncio.sleep(0.5)

# Stop fish servo
def stop():
    task.cancel()

loop = asyncio.get_event_loop()
task = loop.create_task(periodic())

while True:
    read_serial = ser.readline()
    pHValue = float(read_serial.decode().strip())
    print(str(pHValue))
        
    try:
        # loop.run_until_complete(task)
        if (pHValue < 0.0 or pHValue > 14.0):
            continue
        if (pHValue <= 6.0):
            # Turn servo to left
            pwm_pH_servo.ChangeDutyCycle(MAX_DUTY)
            time.sleep(0.5)
        elif (pHValue >= 8.0):       
            # Turn servo to right
            pwm_pH_servo.ChangeDutyCycle(MIN_DUTY)
            time.sleep(0.5)

        # Reset servo to center
        pwm_pH_servo.ChangeDutyCycle(CENTRE)
        time.sleep(0.5)        
    except KeyboardInterrupt:
        print("CTRL-C: Terminating program.")
        print("Cleaning up GPIO...")
        loop.call_later(1, stop)
        pwm_pH_servo.ChangeDutyCycle(CENTRE)
        pwm_feed_servo.ChangeDutyCycle(CENTRE)
        time.sleep(0.5)
        GPIO.cleanup()