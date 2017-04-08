import os
import time
from Voice.GoogleTTS import speak

def setReminder(hours, minutes, Reminder): #Put Threading!!
    not_executed = 1
    while (not_executed):
        dt = list(time.localtime())
        hour = dt[3]
        minute = dt[4]

        print(hour, " ", minute)
        if hour == hours and minute == minutes:
            os.system("mpg321 Glass.mp3")
            speak("Sir, you have " + Reminder)
            print("Reminder executed!")
            break

#setReminder(17,4, "Meeting")