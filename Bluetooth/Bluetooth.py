import serial
from sys import platform as platform
import serial.tools.list_ports
import time
import Gesture
import pyautogui

class Bluetooth():
    input_data = bytes

    def __init__(self):
        print("Bluetooth")

    def isFloat(self, string):
        try:
            return float(string)
        except ValueError:
            return False

    def getOS(self):
        port = "/dev/tty.Right-DevB"

        #LINUX
        if platform == "linux" or platform == "linux2":
            port = "/dev/tty.Right-DevB"

        #MAC OS
        elif platform == "darwin":
            port = "/dev/tty.Right-DevB"

        #WINDOWS
        elif platform == "win32":
            port = "COM6"

        return port


    def captureGesture(self):
        x = ""
        y = ""
        z = ""

        dbOp = Gesture.Database.dbOperation()
        dbOp.create()

        port = self.getOS()

        bluetooth = serial.Serial(port, 115200)
        print("Connected Right Hand Bluetooth")
        bluetooth.flushInput()

        # timeout = time.time() + 5

        while 1:
            self.input_data = bluetooth.readline()

            if (self.input_data.decode()[0] == "@"):

                # Read Finger values
                self.input_data = bluetooth.readline()
                x = self.input_data.decode().rstrip()

                self.input_data = bluetooth.readline()
                y = self.input_data.decode().rstrip()

                self.input_data = bluetooth.readline()
                z = self.input_data.decode().rstrip()

                # Store values in db
                values = [x,y,z]
                bluetooth.close()
                break

        return values

    def bluetoothRight(self):
        x = ""
        y = ""
        z = ""

        port = self.getOS()

        bluetooth = serial.Serial(port, 115200)
        print("Connected Right Hand Bluetooth")
        bluetooth.flushInput()

        #timeout = time.time() + 5

        while 1:
            self.input_data = bluetooth.readline()

            if (self.input_data.decode()[0]=="@"):

                #Read Finger values
                self.input_data = bluetooth.readline()
                x = self.input_data.decode().rstrip()

                self.input_data = bluetooth.readline()
                y = self.input_data.decode().rstrip()

                self.input_data = bluetooth.readline()
                z = self.input_data.decode().rstrip()

                #Compare with values from db
                if(float(x)<-13) and (float(y)<64) and (float(z)<-117):
                   print("YES")
                   pyautogui.typewrite('q', interval=1)

                else:
                    print("NO")