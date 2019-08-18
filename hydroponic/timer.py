from datetime import datetime


class Timer():
    def __init__(self):
        self.interval_time = datetime.now()
        
    def getSecondsDiff(self):
        self.current_time = datetime.now()
        return self.getDateDiffInSeconds(self.current_time, self.interval_time)

    def resetInterval(self):
        self.interval_time = datetime.now()
        
    def getDateDiffInSeconds(self, dt2, dt1):
        timedelta = dt2 - dt1
        return timedelta.days * 24 * 3600 + timedelta.seconds
