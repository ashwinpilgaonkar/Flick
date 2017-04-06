import threading
import pyautogui
import Bluetooth.Bluetooth

class HIDEmulation():

    bluetooth = Bluetooth.Bluetooth.Bluetooth()

    def __init__(self):
        print("E M U L A T I O N")

    def testKey(self):
        threading.Thread(target=self.bluetooth.bluetoothRight).start()
        #threading.Thread(target=self.getData).start()
        #pyautogui.typewrite('tyuiopasdfgfhjjhlkzxcvcvbnm', interval=3)

  #  def getData(self):
  #      while 1:
  #          print(self.bluetooth.input_data)

    def ReadValues(self):
        threading.Thread(target=self.bluetooth.bluetoothRight).start()
        print(self.bluetooth.input_data.decode())
