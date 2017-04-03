import serial
from sys import platform as platform
import serial.tools.list_ports

def bluetoothRight():
    port = "/dev/tty.Right-DevB"
    if platform == "linux" or platform == "linux2":
        #linux
        port = "/dev/tty.Right-DevB"

    elif platform == "darwin":
        # MAC OS X
        port = "/dev/tty.Right-DevB"

    elif platform == "win32":
        # Windows
        port = "COM5"

    bluetooth = serial.Serial(port, 115200)
    print("Connected Right Hand Bluetooth")
    bluetooth.flushInput()
    while 1:
        try:
            input_data = bluetooth.readline()
            try:
                print(input_data.decode())
                print('\n')
            except:
                pass
        except serial.serialutil.SerialException:
            break

    bluetooth.close()
    print("closed BLU right hand!")

#bluetoothRight()