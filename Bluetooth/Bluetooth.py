import serial

def bluetoothRight():
    port = "/dev/tty.HC-05-DevB"
    bluetooth = serial.Serial(port, 9600)
    print("Connected Right Hand Bluetooth")
    bluetooth.flushInput()
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
    print("closed BLU right hand!")