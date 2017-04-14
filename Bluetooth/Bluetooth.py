import traceback

import serial
from sys import platform as platform
import serial.tools.list_ports
import pyautogui
import serial.threaded

def getOS():
    port = "/dev/tty.Right-DevB"

    # LINUX
    if platform == "linux" or platform == "linux2":
        port = "/dev/tty.Right-DevB"

    # MAC OS
    elif platform == "darwin":
        port = "/dev/tty.Right-DevB"

    # WINDOWS
    elif platform == "win32":
        port = "COM4"

    return port

def bluetoothRight(data):
    pass #if data is string c

class Output(serial.threaded.Protocol):

    finger = ""
    counter = 0

    def connection_made(self, transport):
        print("Connect_made")
        self.transport = transport
        print('port opened', transport)
        transport.serial.rts = False

    def data_received(self, data):

        line = data.decode().replace("\r", ",").replace("\n", "")

        x = ""
        y = ""
        z = ""
        fingerchange = "@#$%^"
        length = len(line)

        print(data)

        i = 0
        while (i < length):

            if line[i] in fingerchange:
                i = i + 2
                counter = 0
                x = ""
                y = ""
                z = ""

                while i < length and line[i] not in fingerchange and counter < 3:

                    if (line[i] == ","):
                        counter = counter + 1
                        i = i + 1

                        if (counter == 3) or i>=length:
                            break

                    if (counter == 0):
                        x = x + line[i]

                    if (counter == 1):
                        y = y + line[i]

                    if (counter == 2):
                        z = z + line[i]

                    i = i + 1

                #print("X: " + x)
                print("Y: " + y)
                #print("Z: " + z)

                try:
                    x = int(x)
                    y = int(y)

                    '''
                    if(x>15):
                        pyautogui.moveRel(x, y, duration=0)

                    else:
                        pyautogui.moveRel(-x, -y, duration=0)
                    '''

                except:
                    continue

            else:
                i = i + 1

    '''
        if(data.decode()[0]=="@"):
            self.finger = "@"
            self.counter=0
            print("Thumb")

        if(data.decode()[0]=="#"):
            self.finger = "#"
            self.counter = 0
            print("Index")

        if(data.decode()[0]=="$"):
            self.finger = "$"
            self.counter = 0
            print("Middle")

        if(data.decode()[0]=="%"):
            self.finger = "%"
            self.counter = 0
            print("Ring")

        if(data.decode()[0]=="^"):
            self.finger = "^"
            self.counter = 0
            print("Little")
        '''

    '''
        if(self.finger=="@") and self.counter<3:

            if(float(data.decode())>0):
                pyautogui.moveRel(2, 3, duration=0)

            else:
                pyautogui.moveRel(-2, -3, duration=0)

            self.counter = self.counter+1

        if(data.decode()[0]=="@"):
            self.finger = "@"
            self.counter=0

        if(data.decode()[0]=="#"):
            self.finger = "#"
            self.counter = 0

        if(data.decode()[0]=="$"):
            self.finger = "$"
            self.counter = 0

        if(data.decode()[0]=="%"):
            self.finger = "%"
            self.counter = 0

        if(data.decode()[0]=="^"):
            self.finger = "^"
            self.counter = 0

    def connection_lost(self, exc):
        print('port closed')
        traceback.print_exc(0)
    '''


def main():
    ser = serial.Serial(getOS(), baudrate=115200, timeout=1)

    protocol = serial.threaded.ReaderThread(ser, Output)
    protocol.run()

if __name__ == '__main__':
    main()