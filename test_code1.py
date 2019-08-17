import RPi.GPIO as GPIO
import time
import serial
import asyncio
import pyrebase

# Servo position calibration
MIN_DUTY = 3
MAX_DUTY = 13
CENTRE = MIN_DUTY + (11.5 - MIN_DUTY) / 2

# Servo pin declaration
feed_servo_pin = 18
pH_servo_pin = 22
duty_cycle = CENTRE     # Should be the centre for a SG90

# Configure the Pi to use pin names (i.e. BCM) and allocate I/O
GPIO.setmode(GPIO.BOARD)
GPIO.setup(feed_servo_pin, GPIO.OUT)
GPIO.setup(pH_servo_pin, GPIO.OUT)

# Create PWM channel on the servo pin with a frequency of 50Hz
pwm_pH_servo = GPIO.PWM(pH_servo_pin, 50)
pwm_feed_servo = GPIO.PWM(feed_servo_pin, 50)
pwm_pH_servo.start(duty_cycle)
pwm_feed_servo.start(duty_cycle)

# Change ACM number as found from "ls /dev/tty/ACM*"
ser = serial.Serial("/dev/ttyACM0",9600)
ser.baudrate=9600

config = {
  "apiKey": "AIzaSyCpXmQk0W1pmX6bm2WsfW3aRgn5DRR9HOY",
  "authDomain": "iotpractical5-fcbd9.firebaseapp.com",
  "databaseURL": "https://iotpractical5-fcbd9.firebaseio.com",
  "projectId": "iotpractical5-fcbd9",
  "storageBucket": "",
  "messagingSenderId": "317030629635",
  "appId": "1:317030629635:web:d944180093a9b329"
}

# Async function to perform
# fish feeding at an interval
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

firebase = pyrebase.initialize_app(config)
#Get a reference to the auth service
auth = firebase.auth()
#Log the user in
user = auth.sign_in_with_email_and_password("starmanwtest@gmail.com","19308015sw")
#Get a reference to the database service
db = firebase.database()

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