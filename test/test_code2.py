import RPi.GPIO as GPIO
import time
import serial
import pyrebase
from multiprocessing import Process

# Change ACM number as found from "ls /dev/tty/ACM*"
ser = serial.Serial("/dev/ttyACM0",9600)
ser.baudrate=9600

# Async function to perform
# fish feeding at an interval
def feederInterval():
    # Servo position calibration
    MIN_DUTY = 3
    CENTRE = MIN_DUTY + (11.5 - MIN_DUTY) / 2

    # Servo pin declaration
    feed_servo_pin = 18
    duty_cycle = CENTRE     # Should be the centre for a SG90

    # Configure the Pi to use pin names (i.e. BCM) and allocate I/O
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(feed_servo_pin, GPIO.OUT)

    # Create PWM channel on the servo pin with a frequency of 50Hz
    pwm_feed_servo = GPIO.PWM(feed_servo_pin, 50)
    pwm_feed_servo.start(duty_cycle)

    while True:
        try:
            pwm_feed_servo.ChangeDutyCycle(MIN_DUTY)
            time.sleep(0.5)
            pwm_feed_servo.ChangeDutyCycle(CENTRE)
            time.sleep(0.5)
        except KeyboardInterrupt:
            print("CTRL-C: Terminating feeder.")
            print("Cleaning up GPIO...")
            pwm_feed_servo.ChangeDutyCycle(CENTRE)
            time.sleep(1)
            GPIO.cleanup()
        
def pHSensor():
    # Servo position calibration
    MIN_DUTY = 3
    MAX_DUTY = 13
    CENTRE = MIN_DUTY + (11.5 - MIN_DUTY) / 2

    # Servo pin declaration
    pH_servo_pin = 22
    duty_cycle = CENTRE     # Should be the centre for a SG90

    # Configure the Pi to use pin names (i.e. BCM) and allocate I/O
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pH_servo_pin, GPIO.OUT)

    # Create PWM channel on the servo pin with a frequency of 50Hz
    pwm_pH_servo = GPIO.PWM(pH_servo_pin, 50)
    pwm_pH_servo.start(duty_cycle)
    
    while True:
        '''read_serial = ser.readline()
        pHValue = float(read_serial.decode().strip())
        print(str(pHValue))
        '''
        
        pHValue = 4.0
      
        if (pHValue < 0.0 or pHValue > 14.0):
            continue
        if (pHValue <= 6.0):
            # Turn servo to left
            pwm_pH_servo.ChangeDutyCycle(MAX_DUTY)
            time.sleep(1)
        elif (pHValue >= 8.0):       
            # Turn servo to right
            pwm_pH_servo.ChangeDutyCycle(MIN_DUTY)
            time.sleep(1)

        # Reset servo to center
        pwm_pH_servo.ChangeDutyCycle(CENTRE)
        time.sleep(1)
        
try:
    p1 = Process(target = pHSensor)
    p1.start()
    p2 = Process(target = feederInterval)
    p2.start()
except KeyboardInterrupt:
    print("CTRL-C: Terminating program.")
    print("Cleaning up GPIO...")
    pwm_pH_servo.ChangeDutyCycle(CENTRE)
    pwm_feed_servo.ChangeDutyCycle(CENTRE)
    time.sleep(1)
    GPIO.cleanup()
