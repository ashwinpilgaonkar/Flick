import serial

def bluetoothRight():
    port = "/dev/tty.Right-DevB"
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

bluetoothRight()