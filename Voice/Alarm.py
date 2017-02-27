import os
import time

def setReminder(hours, minutes):
    not_executed = 1
    while (not_executed):
        dt = list(time.localtime())
        hour = dt[3]
        minute = dt[4]

        print(hour, " ", minute)
        if hour == hours and minute == minutes:
            os.system("mpg321 Glass.mp3")
            break
    not_executed = 0
