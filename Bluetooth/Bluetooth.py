import serial
from sys import platform as platform
import serial.tools.list_ports
import serial.threaded
from pymouse import PyMouse
from Voice.GoogleTTS import speak
import threading
import math
import copy
import time
import json


data_repository_right = {

    "id" : [],
    "name" : [],
    "shortcuts" : [],
    "time_period": [],

    "0":[],    #   "max_acc_@R_x" : [],
    "1":[],    #   "max_acc_^R_x": [],
    "2":[],    #   "max_acc_#R_x": [],
    "3":[],    #   "max_acc_$R_x": [],
    "4":[],    #   "max_acc_%R_x": [],

    "5":[],    #   "max_acc_@R_y" : [],
    "6":[],    #   "max_acc_^R_y": [],
    "7":[],    #   "max_acc_#R_y": [],
    "8":[],    #   "max_acc_$R_y": [],
    "9":[],    #   "max_acc_%R_y": [],

    "10":[],    #   "max_acc_@R_z": [],
    "11":[],    #   "max_acc_^R_z": [],
    "12":[],    #   "max_acc_#R_z": [],
    "13":[],    #   "max_acc_$R_z": [],
    "14":[],    #   "max_acc_%R_z": [],

    "15":[],    #   "min_acc_@R_x": [],
    "16":[],    #   "min_acc_^R_x": [],
    "17":[],    #   "min_acc_#R_x": [],
    "18":[],    #   "min_acc_$R_x": [],
    "19":[],    #   "min_acc_%R_x": [],

    "20":[],    #   "min_acc_@R_y": [],
    "21":[],    #   "min_acc_^R_y": [],
    "22":[],    #   "min_acc_#R_y": [],
    "23":[],    #   "min_acc_$R_y": [],
    "24":[],    #   "min_acc_%R_y": [],

    "25":[],    #   "min_acc_@R_z": [],
    "26":[],    #   "min_acc_^R_z": [],
    "27":[],    #   "min_acc_#R_z": [],
    "28":[],    #   "min_acc_$R_z": [],
    "29":[],    #   "min_acc_%R_z": [],

    "30":[],    #   "start_angle_@R_x":[],
    "31":[],    #   "start_angle_^R_x": [],
    "32":[],    #   "start_angle_#R_x": [],
    "33":[],    #   "start_angle_$R_x": [],
    "34":[],    #   "start_angle_%R_x": [],

    "35":[],    #   "start_angle_@R_y": [],
    "36":[],    #   "start_angle_^R_y": [],
    "37":[],    #   "start_angle_#R_y": [],
    "38":[],    #   "start_angle_$R_y": [],
    "39":[],    #   "start_angle_%R_y": [],

    "40":[],    #   "start_angle_@R_z": [],
    "41":[],    #   "start_angle_^R_z": [],
    "42":[],    #   "start_angle_#R_z": [],
    "43":[],    #   "start_angle_$R_z": [],
    "44":[],    #   "start_angle_%R_z": [],

    "45":[],    #   "end_angle_@R_x": [],
    "46":[],    #   "end_angle_^R_x": [],
    "47":[],    #   "end_angle_#R_x": [],
    "48":[],    #   "end_angle_$R_x": [],
    "49":[],    #   "end_angle_%R_x": [],

    "50":[],    #   "end_angle_@R_y": [],
    "51":[],    #   "end_angle_^R_y": [],
    "52":[],    #   "end_angle_#R_y": [],
    "53":[],    #   "end_angle_$R_y": [],
    "54":[],    #   "end_angle_%R_y": [],

    "55":[],    #   "end_angle_@R_z": [],
    "56":[],    #   "end_angle_^R_z": [],
    "57":[],    #   "end_angle_#R_z": [],
    "58":[],    #   "end_angle_$R_z": [],
    "59":[],    #   "end_angle_%R_z": [],
}

data_repository_left = {
    "id": [],
    "name": [],
    "shortcuts": [],
    "time_period": [],

    0: [],  # "max_acc_@L_x" : [],
    1: [],  # "max_acc_^L_x": [],
    2: [],  # "max_acc_#L_x": [],
    3: [],  # "max_acc_$L_x": [],
    4: [],  # "max_acc_%L_x": [],

    5: [],  # "max_acc_@L_y" : [],
    6: [],  # "max_acc_^L_y": [],
    7: [],  # "max_acc_#L_y": [],
    8: [],  # "max_acc_$L_y": [],
    9: [],  # "max_acc_%L_y": [],

    10: [],  # "max_acc_@L_z": [],
    11: [],  # "max_acc_^L_z": [],
    12: [],  # "max_acc_#L_z": [],
    13: [],  # "max_acc_$L_z": [],
    14: [],  # "max_acc_%L_z": [],

    15: [],  # "min_acc_@L_x": [],
    16: [],  # "min_acc_^L_x": [],
    17: [],  # "min_acc_#L_x": [],
    18: [],  # "min_acc_$L_x": [],
    19: [],  # "min_acc_%L_x": [],

    20: [],  # "min_acc_@L_y": [],
    21: [],  # "min_acc_^L_y": [],
    22: [],  # "min_acc_#L_y": [],
    23: [],  # "min_acc_$L_y": [],
    24: [],  # "min_acc_%L_y": [],

    25: [],  # "min_acc_@L_z": [],
    26: [],  # "min_acc_^L_z": [],
    27: [],  # "min_acc_#L_z": [],
    28: [],  # "min_acc_$L_z": [],
    29: [],  # "min_acc_%L_z": [],

    30: [],  # "start_angle_@L_x":[],
    31: [],  # "start_angle_^L_x": [],
    32: [],  # "start_angle_#L_x": [],
    33: [],  # "start_angle_$L_x": [],
    34: [],  # "start_angle_%L_x": [],

    35: [],  # "start_angle_@L_y": [],
    36: [],  # "start_angle_^L_y": [],
    37: [],  # "start_angle_#L_y": [],
    38: [],  # "start_angle_$L_y": [],
    39: [],  # "start_angle_%L_y": [],

    40: [],  # "start_angle_@L_z": [],
    41: [],  # "start_angle_^L_z": [],
    42: [],  # "start_angle_#L_z": [],
    43: [],  # "start_angle_$L_z": [],
    44: [],  # "start_angle_%L_z": [],

    45: [],  # "end_angle_@L_x": [],
    46: [],  # "end_angle_^L_x": [],
    47: [],  # "end_angle_#L_x": [],
    48: [],  # "end_angle_$L_x": [],
    49: [],  # "end_angle_%L_x": [],

    50: [],  # "end_angle_@L_y": [],
    51: [],  # "end_angle_^L_y": [],
    52: [],  # "end_angle_#L_y": [],
    53: [],  # "end_angle_$L_y": [],
    54: [],  # "end_angle_%L_y": [],

    55: [],  # "end_angle_@L_z": [],
    56: [],  # "end_angle_^L_z": [],
    57: [],  # "end_angle_#L_z": [],
    58: [],  # "end_angle_$L_z": [],
    59: [],  # "end_angle_%L_z": [],
}

right_data = {
    0: 0,  #    "acc_@R_x"
    1: 0,  #    "acc_^R_x"
    2: 0,  #    "acc_#R_x"
    3: 0,  #    "acc_$R_x"
    4: 0,  #    "acc_%R_x"


    5: 0,  #    "acc_@R_y"
    6: 0,  #    "acc_^R_y"
    7: 0,  #    "acc_#R_y"
    8: 0,  #    "acc_$R_y"
    9: 0,  #    "acc_%R_y"

    10: 0,  #   "acc_@R_z"
    11: 0,  #   "acc_^R_z"
    12: 0,  #   "acc_#R_z"
    13: 0,  #   "acc_$R_z"
    14: 0,  #   "acc_%R_z"

    15: 0,    # "angle_@R_x"
    16: 0,    # "angle_^R_x"
    17: 0,    # "angle_#R_x"
    18: 0,    # "angle_$R_x"
    19: 0,    # "angle_%R_x"

    20: 0,    # "angle_@R_y"
    21: 0,    # "angle_^R_y"
    22: 0,    # "angle_#R_y"
    23: 0,    # "angle_$R_y"
    24: 0,    # "angle_%R_y"

    25: 0,    # "angle_@R_z"
    26: 0,    # "angle_^R_z"
    27: 0,    # "angle_#R_z"
    28: 0,    # "angle_$R_z"
    29: 0    # "angle_%R_z"
}

left_data = {
    0: 0,  # "acc_@L_x"
    1: 0,  # "acc_^L_x"
    2: 0,  # "acc_#L_x"
    3: 0,  # "acc_$L_x"
    4: 0,  # "acc_%L_x"


    5: 0,  # "acc_@L_y"
    6: 0,  # "acc_^L_y"
    7: 0,  # "acc_#L_y"
    8: 0,  # "acc_$L_y"
    9: 0,  # "acc_%L_y"

    10: 0,  # "acc_@L_z"
    11: 0,  # "acc_^L_z"
    12: 0,  # "acc_#L_z"
    13: 0,  # "acc_$L_z"
    14: 0,  # "acc_%L_z"

    15: 0,  # "angle_@L_x"
    16: 0,  # "angle_^L_x"
    17: 0,  # "angle_#L_x"
    18: 0,  # "angle_$L_x"
    19: 0,  # "angle_%L_x"

    20: 0,  # "angle_@L_y"
    21: 0,  # "angle_^L_y"
    22: 0,  # "angle_#L_y"
    23: 0,  # "angle_$L_y"
    24: 0,  # "angle_%L_y"

    25: 0,  # "angle_@L_z"
    26: 0,  # "angle_^L_z"
    27: 0,  # "angle_#L_z"
    28: 0,  # "angle_$L_z"
    29: 0  # "angle_%L_z"
}

pre_right_data = copy.deepcopy(right_data)
pre_left_data = copy.deepcopy(left_data)

average_right_data = copy.deepcopy(right_data)

movement_Sensitivity_x= 2
movement_Sensitivity_y= 2
movement_Sensitivity_z= 2

threshold_movement_Sensitivity = 14000
recognition_Gap_Interval = 200
initial_Gap_Interval = 200

angle_tolerance = 5
acc_tolerance = 0.5

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

def bluetooth(serRight, serLeft, recognitionFlag=0):
        global pre_right_data
        global pre_left_data
        global  average_right_data
        global right_data
        global left_data
        global  data_repository_right
        iteration_Count = 0
        averageFlag = True

        #------Recognition variables--------------
        recognitionCount = 0
        recognitionGapCount = 0
        start_time = 0
        recognitionMode = False
        #Get current id
        try:
            curr_id = data_repository_right["id"][-1] + 1
        except:
            curr_id = 0
        initialize_data_repository_right()

        while True:
            # %: Pinky finger, ^: index finger, @: thumb, $: ring
#-------------RIGHT HAND--------------------------------
            try:
                line = serRight.readline()
                line = line.decode('utf-8')
                line = line.strip('\r')
                line = line.strip('\n')

                if "@" in line:              #THUMB
                    #print(line[0])
                    right_data[0] = get_data(serRight)
                    #print(right_data[0])
                    right_data[5] = get_data(serRight)  # Meter per seconds square
                    #print(right_data[5])
                    right_data[10] = get_data(serRight)
                    #print(right_data[10])
                    right_data[15] = get_data(serRight)
                    #print(right_data[15])
                    right_data[20] = get_data(serRight) # Angle in degrees
                    #print(right_data[20])
                    right_data[25] = get_data(serRight)
                    #print(right_data[25])

                elif "^" in line:            #INDEX FINGER
                    #print(line[0])
                    right_data[1] = get_data(serRight)
                    #print(right_data[1])
                    right_data[6] = get_data(serRight)  # Meter per seconds square
                    #print(right_data[6])
                    right_data[11] = get_data(serRight)
                    #print(right_data[11])
                    right_data[16] = get_data(serRight)
                    #print(right_data[16])
                    right_data[21] = get_data(serRight)  # Angle in degrees
                    #print(right_data[21])
                    right_data[26] = get_data(serRight)
                    #print(right_data[26])


                elif "#" in line:            #MIDDLE FINGER
                    #print(line[0])
                    right_data[2] = get_data(serRight)
                    #print(right_data[2])
                    right_data[7] = get_data(serRight)  # Meter per seconds square
                    #print(right_data[7])
                    right_data[12] = get_data(serRight)
                    #print(right_data[12])
                    right_data[17] = get_data(serRight)
                    #print(right_data[17])
                    right_data[22] = get_data(serRight)  # Angle in degrees
                    #print(right_data[22])
                    right_data[27] = get_data(serRight)
                    #print(right_data[27])

                elif "$" in line:            #RING FINGER
                    #print(line[0])
                    right_data[3] = get_data(serRight)
                    #print(right_data[3])
                    right_data[8] = get_data(serRight)  # Meter per seconds square
                    #print(right_data[8])
                    right_data[13] = get_data(serRight)
                    #print(right_data[13])
                    right_data[18] = get_data(serRight)
                    #print(right_data[18])
                    right_data[23] = get_data(serRight)  # Angle in degrees
                    #print(right_data[23])
                    right_data[28] = get_data(serRight)
                    #print(right_data[28])



                elif "%" in line:            #PINKY FINGER
                    #print(line[0])
                    right_data[4] = get_data(serRight)
                    #print(right_data[4])
                    right_data[9] = get_data(serRight)  # Meter per seconds square
                    #print(right_data[9])
                    right_data[14] = get_data(serRight)
                    #print(right_data[14])
                    right_data[19] = get_data(serRight)
                    #print(right_data[19])
                    right_data[24] = get_data(serRight)  # Angle in degrees
                    #print(right_data[14])
                    right_data[29] = get_data(serRight)
                    #print(right_data[29])

            except Exception as e:
                print("Exception", format(e))
                pass
                # Refining by taking average of values

            if iteration_Count < initial_Gap_Interval and averageFlag == True:
                count = 0
                for curr_Key in right_data:
                    if count > 14: break
                    average_right_data[curr_Key] += right_data[curr_Key]

            elif iteration_Count >= initial_Gap_Interval and averageFlag == True:
                count = 0
                for curr_Key in right_data:
                    if count > 14: break
                    try:
                        average_right_data[curr_Key] /= initial_Gap_Interval
                    except:
                        pass
                    count += 1
                averageFlag = False
            elif iteration_Count >= initial_Gap_Interval and averageFlag == False:
                count = 0
                for curr_Key in right_data:
                    if count > 14: break
                    try:
                        right_data[curr_Key] /= average_right_data[curr_Key]
                    except:
                        pass
                    count += 1

            if recognitionFlag != 1:
                for eachID in data_repository_right["id"]:
                    fingerCount = 0                         #Finger Recognised count
                    for max_x, max_y, max_z, min_x, min_y, min_z, start_angle_x, start_angle_y, start_angle_z, right_x, right_y, right_z, right_angle_x, right_angle_y, right_angle_z in zip(list(range(0,5)), list(range(5, 10)), list(range(10, 15)), list(range(15, 20)), list(range(20, 25)), list(range(25, 30)), list(range(30, 35)), list(range(35, 40)), list(range(40, 45)), list(range(0, 5)), list(range(5, 10)),list(range(10, 15)),list(range(15, 20)),list(range(20, 25)),list(range(25, 30))):
                        if          (right_data[right_x] > data_repository_right[str(max_x)][eachID] - acc_tolerance)\
                                and (right_data[right_x] < data_repository_right[str(max_x)][eachID] + acc_tolerance)\
                                and (right_data[right_y] > data_repository_right[str(max_y)][eachID] - acc_tolerance)\
                                and (right_data[right_y] < data_repository_right[str(max_y)][eachID] + acc_tolerance)\
                                and (right_data[right_z] > data_repository_right[str(max_z)][eachID] - acc_tolerance)\
                                and (right_data[right_z] < data_repository_right[str(max_z)][eachID] + acc_tolerance)\
                                and (right_data[right_angle_x] < (data_repository_right[str(start_angle_x)][eachID] + angle_tolerance))\
                                and (right_data[right_angle_x] > (data_repository_right[str(start_angle_x)][eachID] - angle_tolerance))\
                                and (right_data[right_angle_y] < (data_repository_right[str(start_angle_y)][eachID] + angle_tolerance))\
                                and (right_data[right_angle_y] > (data_repository_right[str(start_angle_y)][eachID] - angle_tolerance))\
                                and (right_data[right_angle_z] < (data_repository_right[str(start_angle_z)][eachID] + angle_tolerance))\
                                and (right_data[right_angle_z] > (data_repository_right[str(start_angle_z)][eachID] - angle_tolerance)):

                            fingerCount += 1

                    if fingerCount == 3:
                        print("Initial condition true")
                    else:
                        print("not matched", "\t", fingerCount)
                    #print(data_repository_right, end="\n\n")
                    #print(right_data, end="\n\n")
 # ----------------RECOGNITION----------------------------

                i=0
                j=0
                pos=0
                match = False
                while(i<len(data_repository_right.get(0))):
                    while(j+15<60):
                        #If current data of Thumb (angles and accln) is greater than min and less than max value
                        if(right_data.get(j) < data_repository_right.get(j)[i]) and (right_data.get(j) > data_repository_right.get(j+15)[i]):
                            pos = i
                            match = True

                        else:
                            match = False

                        j = j+5

                        if (j==15):
                            j=30
                i+=1

                if match:
                    shortcut = data_repository_right.get("shortcuts")[pos]
                    #Implement Shortcut


            if recognitionFlag == 1 and iteration_Count > initial_Gap_Interval:
                if recognitionCount > 5:
                    print(data_repository_right)
                    print("Ok Recognized")

                    recognitionFlag = 0
                    try:
                        with open('DataRepositoryRight.json', 'w') as outfile:
                            json.dump(data_repository_right, outfile)
                    except:
                        print("Could not write DataRepositoryRight.json")

                    #return
                else: print("Repeat", recognitionCount)
                curr_time = time.time()

                for x_values, y_values, z_values in zip(list(range(5)), list(range(5, 10)),list(range(10, 15))):
                 #only x, y, z acceleration values of each finger
                    if math.fabs(right_data[x_values]) > movement_Sensitivity_x and math.fabs(right_data[y_values]) > movement_Sensitivity_y and math.fabs(right_data[z_values]) > movement_Sensitivity_z:
                        if recognitionMode == False:
                            print("Recognition period ON", "True")
                            start_time = curr_time
                            store_gesture(False, "right",name="Dummy", shortcuts="dummy", curr_id= curr_id)
                            recognitionMode = True

                    elif recognitionMode == True and recognitionGapCount > recognition_Gap_Interval:
                        recognitionMode = False
                        time_period = curr_time - start_time
                        store_gesture(True, "right", time=time_period , curr_id=curr_id)
                        print("Recognition period OFF", "False")
                        recognitionCount += 1
                        recognitionGapCount = 0
                        break

#----------------------------------------END----------------

            pre_right_data = copy.deepcopy(right_data)
            pre_left_data = copy.deepcopy(left_data)
            iteration_Count += 1
            if recognitionMode == True:
                recognitionGapCount += 1

def initialize_data_repository_right():
    global  data_repository_right
    data_repository_right["id"].append(0)
    data_repository_right["name"].append(" ")
    data_repository_right["shortcuts"].append(" ")
    data_repository_right["time_period"].append(0)
    for i in list(range(60)):
        data_repository_right[str(i)].append(0)

def store_gesture(recognitionModeEnd, hand="right", time= 0, name="Dummy", shortcuts="dummy", curr_id = 0):
    if hand == "right":
        if recognitionModeEnd == False:
            data_repository_right["id"][curr_id] = curr_id
            data_repository_right["name"][curr_id] = name
            data_repository_right["shortcuts"][curr_id] = shortcuts

            for i in list(range(15)):                                           # Max Acceleration
            #    val = get_data_from_Data_Repository(str(i), curr_id)
            #    if val < right_data[i]:
                    data_repository_right[str(i)][curr_id] = right_data[i]

            for i, j in zip(list(range(15,30)), list(range(15))):                    #Min Acceleration
             #   val = get_data_from_Data_Repository(str(i), curr_id)
             #   if val > right_data[j] or val == 0:
                    data_repository_right[str(i)][curr_id] = right_data[j]

            for i, j in zip(list(range(30, 45)), list(range(15, 30))):          #Start Index
 #               val = get_data_from_Data_Repository(str(i),curr_id)
                #if val == 0:
                #   data_repository_right[str(i)][curr_id] = right_data[j]
                #else:
                data_repository_right[str(i)][curr_id] = right_data[j]  #Average

#------------------------------------------------------------------------------------------------
        elif recognitionModeEnd == True:
            for i, j in zip(list(range(45, 60)), list(range(15, 30))):               #End Index
#                val = get_data_from_Data_Repository(str(i), curr_id)
 #               if val == 0:
  #                  data_repository_right[str(i)][curr_id] = right_data[j]
   #             else:
                data_repository_right[str(i)][curr_id] = right_data[j]

    #        val = get_data_from_Data_Repository("time_period", curr_id)
    #        if val == 0:
                data_repository_right["time_period"][curr_id] = time  # Time period
     #       else:
      #          data_repository_right["time_period"][curr_id] = (time + val) / 2  # Time period


    elif hand == "left":
        pass
    return

def get_data_from_Data_Repository(key, curr_id):
    global data_repository_right
    try:
        val = data_repository_right[key][curr_id]
    except:
        val = 0
    return val

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

def gesture_Recognition():
        global data_repository_right
        global data_repository_left

#Left and Right hand connection---------------------------------------------------------

        serRight = serial.Serial(get_OS_Right(), baudrate=115200, timeout=1)
        print("Connected Right")
#        serLeft = serial.Serial(get_OS_Left(), baudrate=115200, timeout=1)
 #       print("Connected Left")
#Load Data repository -----------------------------------------------------------------------

        try:
            with open('DataRepositoryRight.json', 'r') as inputFile:
                data_repository_right = json.load(inputFile)
        except:
            print("DataRepositoryRight.json file not found")

        try:
            with open('DataRepositoryLeft.json', 'r') as inputFile:
                data_repository_left = json.load(inputFile)
        except:
            print("DataRepositoryLeft.json file not found")
#Connection-----------------------------------------------------------------------------------------

        if serRight.isOpen():# or serLeft.isOpen():
            bluetooth(serRight,0, recognitionFlag=0)
        else:
            print("Both are unreachable")

        return 0

def main():
    pass

if __name__ == '__main__':
    gesture_Recognition()
