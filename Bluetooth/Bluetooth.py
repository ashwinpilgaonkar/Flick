import serial
from sys import platform as platform
import serial.tools.list_ports
import serial.threaded
from pymouse import PyMouse


def get_OS_Right():
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

def get_OS_Left():
    port = "/dev/tty.LEFT-DevB"

    # LINUX
    if platform == "linux" or platform == "linux2":
        port = "/dev/tty.LEFT-DevB"

    # MAC OS
    elif platform == "darwin":
        port = "/dev/tty.LEFT-DevB"

    # WINDOWS
    elif platform == "win32":
        port = "COM4"

    return port

right_data = {
    "acc_@_x": 0,
    "acc_@_y": 0,
    "acc_@_z": 0,
    "angle_@_x": 0,
    "angle_@_y": 0,
    "angle_@_z": 0,

    "acc_^_x": 0,
    "acc_^_y": 0,
    "acc_^_z": 0,
    "angle_^_x": 0,
    "angle_^_y": 0,
    "angle_^_z": 0,

    "acc_#_x": 0,
    "acc_#_y": 0,
    "acc_#_z": 0,
    "angle_#_x": 0,
    "angle_#_y": 0,
    "angle_#_z": 0,

    "acc_$_x": 0,
    "acc_$_y": 0,
    "acc_$_z": 0,
    "angle_$_x": 0,
    "angle_$_y": 0,
    "angle_$_z": 0,

    "acc_%_x": 0,
    "acc_%_y": 0,
    "acc_%_z": 0,
    "angle_%_x": 0,
    "angle_%_y": 0,
    "angle_%_z": 0,

}

left_data = {
    "acc_@_x": 0,
    "acc_@_y": 0,
    "acc_@_z": 0,
    "angle_@_x": 0,
    "angle_@_y": 0,
    "angle_@_z": 0,

    "acc_^_x": 0,
    "acc_^_y": 0,
    "acc_^_z": 0,
    "angle_^_x": 0,
    "angle_^_y": 0,
    "angle_^_z": 0,

    "acc_#_x": 0,
    "acc_#_y": 0,
    "acc_#_z": 0,
    "angle_#_x": 0,
    "angle_#_y": 0,
    "angle_#_z": 0,

    "acc_$_x": 0,
    "acc_$_y": 0,
    "acc_$_z": 0,
    "angle_$_x": 0,
    "angle_$_y": 0,
    "angle_$_z": 0,

    "acc_%_x": 0,
    "acc_%_y": 0,
    "acc_%_z": 0,
    "angle_%_x": 0,
    "angle_%_y": 0,
    "angle_%_z": 0,

}

def bluetooth(serRight):
    while True:
        # %: Pinky finger, ^: index finger, @: thumb, $: ring
        try:
            line = serRight.readline()
            line = line.decode()
            line = line.strip('\r')
            line = line.strip('\n')

            try:
                if line[0] == "@":              #THUMB
                    right_data["acc_@_x"] = get_data(serRight)
                    right_data["acc_@_y"] = get_data(serRight)  # Meter per seconds square
                    right_data["acc_@_z"] = get_data(serRight)
                    right_data["angle_@_x"] = get_data(serRight)
                    right_data["angle_@_y"] = get_data(serRight) # Angle in degrees
                    right_data["angle_@_z"] = get_data(serRight)

                elif line[0] == "^":            #INDEX FINGER
                    right_data["acc_^_x"] = get_data(serRight)
                    right_data["acc_^_y"] = get_data(serRight)  # Meter per seconds square
                    right_data["acc_^_z"] = get_data(serRight)
                    right_data["angle_^_x"] = get_data(serRight)
                    right_data["angle_^_y"] = get_data(serRight)  # Angle in degrees
                    right_data["angle_^_z"] = get_data(serRight)


                elif line[0] == "#":            #MIDDLE FINGER
                    right_data["acc_#_x"] = get_data(serRight)
                    right_data["acc_#_y"] = get_data(serRight)  # Meter per seconds square
                    right_data["acc_#_z"] = get_data(serRight)
                    right_data["angle_#_x"] = get_data(serRight)
                    right_data["angle_#_y"] = get_data(serRight)  # Angle in degrees
                    right_data["angle_#_z"] = get_data(serRight)

                elif line[0] == "$":            #RING FINGER
                    right_data["acc_$_x"] = get_data(serRight)
                    right_data["acc_$_y"] = get_data(serRight)  # Meter per seconds square
                    right_data["acc_$_z"] = get_data(serRight)
                    right_data["angle_$_x"] = get_data(serRight)
                    right_data["angle_$_y"] = get_data(serRight)  # Angle in degrees
                    right_data["angle_$_z"] = get_data(serRight)

                elif line[0] == "%":            #PINKY FINGER
                    right_data["acc_%_x"] = get_data(serRight)
                    right_data["acc_%_y"] = get_data(serRight)  # Meter per seconds square
                    right_data["acc_%_z"] = get_data(serRight)
                    right_data["angle_%_x"] = get_data(serRight)
                    right_data["angle_%_y"] = get_data(serRight)  # Angle in degrees
                    right_data["angle_%_z"] = get_data(serRight)

            except:
                pass
                # Wait for the character to come
            print(right_data , end='\n\n')
        except:
            return 1

def mouse(acc_x, acc_y, acc_z, angle_x, angle_y, angle_z, pre_coor_x, pre_coor_y):
    # Condition for mouse
    '''
    current_coor_x = dim_x
    current_coor_y = dim_y

    pre_coor_x = 0
    pre_coor_y = 0
    '''

    m = PyMouse()
    dim_x, dim_y = m.screen_size()
    sensitivity = 10000 * 1.5 #between



    pixel_accel_x = (angle_x * 3779.5275591) / sensitivity  # pixel per second square
    pixel_accel_y = (angle_y * 3779.5275591) / sensitivity
    pixel_accel_z = (angle_z * 3779.5275591) / sensitivity

    temp_dist_x = 0.5 * pixel_accel_x
    temp_dist_y = 0.5 * pixel_accel_y

    if temp_dist_x + pre_coor_x <= dim_x and temp_dist_x + pre_coor_x >= 0:
        current_coor_x = int(pre_coor_x + temp_dist_x)

    if temp_dist_y + pre_coor_y <= dim_y and temp_dist_y + pre_coor_y >= 0:
        current_coor_y = int(pre_coor_y + temp_dist_y)

    #m.move(current_coor_x, current_coor_y)

    print(current_coor_x, "\t", current_coor_y)

    pre_coor_x = current_coor_x
    pre_coor_y = current_coor_y

    return pre_coor_x, pre_coor_y

def get_data(ser):
    line = ser.readline()
    line = line.decode()
    line = line.strip('\r')
    line = line.strip('\n')
    try:
        return int(line)
    except: return 0

def main():
    for i in list(range(5)):
        try:
            flag = 0
            serRight = serial.Serial(get_OS_Right(), baudrate=115200, timeout=1)
            flag = bluetooth(serRight)
            if flag != 1:
                break
            print("device failed to connect. Reconnecting....")
        except:
            pass
    print("Failed to reconnect")


    '''serLeft = serial.Serial(get_OS_Left(), baudrate= 115200, timeout=5)
    print("Success")
    while True:
        print(serLeft.readline())
        print("print")'''
if __name__ == '__main__':
    main()