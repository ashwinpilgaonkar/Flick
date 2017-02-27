import serial

port = "/dev/tty.HC-05-DevB"
bluetooth = serial.Serial(port,9600)
print("Connected")
bluetooth.flushInput()
print("Readable: ")
print(bluetooth.readable())

print("Entering loop")
while 1:
    input_data = bluetooth.readline()
    try:
        try:
            print(input_data.decode())
            print('\n')
        except:
            pass
    except serial.serialutil.SerialException:
        break

bluetooth.close()
print("close")