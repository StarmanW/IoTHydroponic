import time
from timer import Timer

def fishFeeder():
    try:
        print("feederInterval")
    except Exception:
        print("Error")


def pHSensor():
    try:
        print("pHSensor")
        time.sleep(1)
    except Exception:
        print("Error")

if __name__ == '__main__':
    timer = Timer()
    while True:
        try:
            pHSensor()
            if (timer.getSecondsDiff() == 10):
                timer.resetInterval()
                fishFeeder()
        except KeyboardInterrupt:
            print("CTRL-C: Terminating program.")
            break