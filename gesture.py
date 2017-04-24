up_Flag = False
down_Flag = False
left_Flag = False
right_Flag = False
keyBoard = PyKeyboard()
from pykeyboard import PyKeyboard

if iteration_Count > initial_Gap_Interval:
    nfs(right_data)


def nfs(right_data):
    global up_Flag
    global left_Flag
    global down_Flag
    global right_Flag

    if right_data[16] < -60 and left_Flag is False: #Move Left
        left_Flag = True
        print("Left")
        keyBoard.press_key("a")

    else:
        left_Flag = False
        keyBoard.release_key("a")

    if right_data[16] > 20 and right_Flag is False: #Move Right
        print("Right")
        right_Flag = True
        keyBoard.press_key("d")

    else :
        pass
        right_Flag = False
        keyBoard.release_key("d")

    if right_data[21] < 0 and up_Flag is False: #Move Forward
        print("Forward")
        up_Flag = True
        keyBoard.press_key("w")

    else:
        up_Flag = False
        keyBoard.release_key("w")

    if right_data[21] > 20 and down_Flag is False: #Move Backward
        print("Backward")
        down_Flag = True
        keyBoard.press_key("s")

    else:
        down_Flag = False
        keyBoard.release_key("s")
