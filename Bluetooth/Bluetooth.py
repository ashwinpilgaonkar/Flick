import serial
from sys import platform as platform
import serial.tools.list_ports
import serial.threaded
from pymouse import PyMouse
import time
import pyautogui as pa

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

def bluetooth(serRight):
    characters = "$#@^%"

    m = PyMouse()
    dim_x, dim_y = m.screen_size()

    current_coor_x = dim_x
    current_coor_y = dim_y

    pre_coor_x = 0
    pre_coor_y = 0

    pre_time = time.time()

    sensitivity = 10000 * 1.5  # between

    while True:
        # Code for right hand
        try:
            line = serRight.readline()
            line = line.decode()
            line = line.strip('\r')
            line = line.strip('\n')

            try:
                if line[0] in characters:
                    print(line[0])
                    x = get_data(serRight)
                    y = get_data(serRight) # Meter per seconds square
                    z = get_data(serRight)

                    pixel_accel_x = (x * 3779.5275591) /sensitivity #pixel per second square
                    pixel_accel_y = (y * 3779.5275591) / sensitivity
                    pixel_accel_z = (z * 3779.5275591) /sensitivity

                    #print("x: ", pixel_accel_x)
                    #print("y: ", pixel_accel_y)
                    #print("z: ", pixel_accel_z)
                    curr_time = time.time()
                    delta_time = curr_time - pre_time
                    temp_dist_x = 0.5 * pixel_accel_x * delta_time *delta_time
                    temp_dist_y = 0.5 * pixel_accel_y * delta_time *delta_time

                    if temp_dist_x + pre_coor_x <= dim_x and temp_dist_x + pre_coor_x >= 0:
                        current_coor_x = int(pre_coor_x + temp_dist_x) #* delta_time * delta_time

                    if temp_dist_y + pre_coor_y <= dim_y and temp_dist_y + pre_coor_y >= 0:
                        current_coor_y = int(pre_coor_y + temp_dist_y) #* delta_time * delta_time

                    m.move(current_coor_x, current_coor_y)
                    print(current_coor_x, "\t",current_coor_y)

                    pre_coor_x = current_coor_x
                    pre_coor_y = current_coor_y

                    pre_time = curr_time
            except:
                pass
        except:
            return 1

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
            serRight = serial.Serial(getOS(), baudrate=115200, timeout=1)
            flag = bluetooth(serRight)
            if flag != 1:
                break
            print("device failed to connect. Reconnecting....")
        except:
            pass
    print("Failed to reconnect")

if __name__ == '__main__':
    main()