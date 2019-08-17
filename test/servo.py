import RPi.GPIO as GPIO

class Servo():
    # Servo position calibration
    MIN_DUTY = 3
    MAX_DUTY = 13
    CENTRE = MIN_DUTY + (11.5 - MIN_DUTY) / 2
    DUTY_CYCLE = CENTRE

    def __init__(self, servo_pin):
        self.servo_pin = servo_pin

        # Configure the Pi to use pin names (i.e. BCM) and allocate I/O
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.servo_pin, GPIO.OUT)
        
        # Create PWM channel on the servo pin with a frequency of 50Hz
        self.pwm_channel = GPIO.PWM(self.servo_pin, 50)
        self.pwm_channel.start(Servo.DUTY_CYCLE)

    # Rotate servo to left
    def rotateLeft(self):
        self.pwm_channel.ChangeDutyCycle(Servo.MAX_DUTY)

    # Rotate servo to right
    def rotateRight(self):
        self.pwm_channel.ChangeDutyCycle(Servo.MIN_DUTY)

    # Rotate servo to center
    def rotateCenter(self):
        self.pwm_channel.ChangeDutyCycle(Servo.CENTRE)
