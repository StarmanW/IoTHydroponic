import RPi.GPIO as GPIO
import time

MIN_DUTY = 3
MAX_DUTY = 13
CENTRE = MIN_DUTY + (11.5 - MIN_DUTY) / 2

servo_pin = 22
duty_cycle = CENTRE     # Should be the centre for a SG90

# Configure the Pi to use pin names (i.e. BCM) and allocate I/O
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo_pin, GPIO.OUT)

# Create PWM channel on the servo pin with a frequency of 50Hz
pwm_servo = GPIO.PWM(servo_pin, 50)
pwm_servo.start(duty_cycle)

while True:    
    try:
        testpHValue = 8.5
        if (testpHValue <= 6.0):
            # Turn servo to left
            pwm_servo.ChangeDutyCycle(MAX_DUTY)
            time.sleep(0.5)
        elif (testpHValue >= 8.0):       
            # Turn servo to right
            pwm_servo.ChangeDutyCycle(MIN_DUTY)
            time.sleep(0.5)

        # Reset servo to center
        pwm_servo.ChangeDutyCycle(CENTRE)
        time.sleep(0.5)        
    except KeyboardInterrupt:
        print("CTRL-C: Terminating program.")
    finally:
        print("Cleaning up GPIO...")
        pwm_servo.ChangeDutyCycle(CENTRE)
        time.sleep(0.5)
        GPIO.cleanup()
