import serial
import time

port = "/dev/tty.HC-05-DevB"
bluetooth = serial.Serial(port,9600)
print("Connected")
bluetooth.flushInput()

while 1:
    input_data = bluetooth.readline()
    print(input_data.decode())
    time.sleep(0.1)

bluetooth.close()
print("close")