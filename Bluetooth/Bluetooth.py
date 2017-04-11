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
        port = "COM6"

    return port

def bluetoothRight(data):
    pass #if data is string c

class Output(serial.threaded.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        print('port opened', transport)
        transport.serial.rts = False

    def data_received(self, data):
        try:
            print(float(data.decode().rstrip()))
        except:
            print(data.decode().rstrip())

        pyautogui.moveRel(0,0,duration=0)

    def connection_lost(self, exc):
        print('port closed')
        traceback.print_exc(0)

def main():
    ser = serial.Serial(getOS(), baudrate=115200, timeout=1)
    protocol = serial.threaded.ReaderThread(ser, Output)
    protocol.run()



if __name__ == '__main__':
    main()