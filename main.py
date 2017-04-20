import sys
from PyQt5.QtWidgets import *
from Voice.SpeechRecognition import listen
import UI.MainWindow
import Gesture.Database
#import Gesture.HIDEmulation
import threading
#from Bluetooth import *
import asyncio
from Voice.Likelyhood_Selection import bernoulli_Selection
from Voice.SelectTask import *



class MainWindow(QMainWindow, UI.MainWindow.Ui_MainWindow, QTableWidget):

    DropDownText=""
    values = None
    combo = list()
    loop = asyncio.get_event_loop()

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        #Initialize Gesture Page UI Elements
        self.ReadGestureButton.clicked.connect(self.ReadGestureButton_OnClick)
        self.CaptureGestureButton.clicked.connect(self.CaptureGestureButton_OnClick)
        self.AddButton.clicked.connect(self.AddButton_OnClick)
        self.ClearButton.clicked.connect(self.ClearButton_OnClick)
        self.SaveButton.clicked.connect(self.SaveButton_OnClick)
        self.FunctionDropdown.addItems(["Ctrl", "Alt", "Esc", "Tab", "Space", "Enter", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "a", "s", "d", "f", "g", "h", "j", "k", "l", "z", "x", "c", "v", "b", "n", "m", "`", "-", "=", "+", "/", "*", ",", ".", ";", "'", "[", "]"])

        #initialize Voice Page UI Elements
        self.TalkButton.clicked.connect(self.TalkButton_OnClick)

        #Initialize dbTable UI View
        self.updateDbTable()

    def updateDbTable(self):
        dbOp = Gesture.Database.dbOperation()
        dbOp.create()
        items = dbOp.read()

        self.dbTable.setColumnCount(3)
        self.dbTable.setHeaderLabels(["ID", "Name", "Shortcut"])
        self.dbTable.clear()
        self.dbTable.resizeColumnToContents(0)

        i=0
        while(i+2<len(items)):
            list = QTreeWidgetItem([str(items[i]), str(items[i+1]), str(items[i+2])])
            self.dbTable.addTopLevelItem(list)
            i=i+3

    def ReadGestureButton_OnClick(self):
        print("Read Gesture")
        self.StatusLabel.setText("Reading...")
        #self.values = Bluetooth.Bluetooth.Bluetooth().captureGesture()

    def CaptureGestureButton_OnClick(self):
        print("Capture Gesture")
        self.StatusLabel.setText("Captured!")

    def AddButton_OnClick(self):
        self.combo.append(self.FunctionDropdown.currentText())

        text = ""
        i=0
        while(i<len(self.combo)):
            text = text + self.combo[i] + " + "
            i=i+1
        text = text[:-3]

        self.ComboLabel.setText(text)

    def ClearButton_OnClick(self):
        self.combo.clear()
        self.GestureName.setText("Name")
        self.ComboLabel.setText("None")

    def SaveButton_OnClick(self):
        text = ""
        i=0
        while(i<len(self.combo)):
            text = text + self.combo[i] + " + "
            i=i+1
        text = text[:-3]

        gesture_name = self.GestureName.text()
        print(gesture_name)

        dbOp = Gesture.Database.dbOperation()
        dbOp.create()
        dbOp.read()
        count = dbOp.getCount()
        #dbOp.insert(count+1, "ADS", "QWE", self.values[0], self.values[1], self.values[2], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        dbOp.insert(count+1, gesture_name, text, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

        self.updateDbTable()
        print("Save")

    def TalkButton_OnClick(self):
        #Convert listened speech to text
        self.VoiceLabel.setText("Listening...")
        future = asyncio.Future()
        asyncio.ensure_future(listen(future))
        future.add_done_callback(self.speech_recognition_complete)
        thread = threading.Thread(target=self.speech_recognition_start, args=(future,))
        thread.start()

    def speech_recognition_start(self, future):
        try:
            self.loop.run_until_complete(future=future)
        except:
            self.VoiceLabel.setText("Speech recognition could not start")

    def speech_recognition_complete(self, future):
        try:
            text = str(future.result())
            if text == "1":
                self.VoiceLabel.setText("Google failed to understand the audio.")
            else:
                self.VoiceLabel.setText(text)
                if "type" in text.split() or "types" in text.split() or "tap" in text.split() or "mode" in text.split() or "typ" in text.split() :
                    self.progressBar_Type.setValue(100)
                    self.VoiceLabel.setText("Type mode ON")
                    loop = asyncio.get_event_loop()
                    future = asyncio.Future()
                    TypeInformation(loop, future=future)
                else:
                    index, similarity  = bernoulli_Selection(text)
                    print(index)
                    if index == 1:
                        self.progressBar_Search.setValue(similarity * 100)
                    elif index == 2:
                        self.progressBar_ScreenShot.setValue(similarity * 100)
                    elif index == 3:
                        self.progressBar_Type.setValue(similarity * 100)
                    elif index == 4:
                        self.progressBar_Youtube.setValue(similarity * 100)
                    elif index == 5:
                        self.progressBar_News.setValue(similarity * 100)
                    elif index == 6:
                        self.progressBar_Reminder.setValue(similarity * 100)
                    else:
                        self.progressBar_email.setValue(similarity * 100)

                    future.done()
        except:
             self.VoiceLabel.setText("Something went wrong. Restart the application")

        return



def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()