import serial
from sys import platform as platform
import serial.tools.list_ports
import pyautogui
import asyncio
import serial.aio
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

class Output(asyncio.Protocol):
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
        asyncio.get_event_loop().stop()

def main():
    while loop.is_running():
        loop = asyncio.get_event_loop()
        coro = serial.aio.create_serial_connection(loop, Output, getOS(), baudrate=115200)
        loop.run_until_complete(coro)
        loop.run_forever()
        loop.close()

if __name__ == '__main__':
    main()