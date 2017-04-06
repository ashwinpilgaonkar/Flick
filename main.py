import sys
from PyQt5.QtWidgets import *
from Voice.SpeechRecognition import listen
import UI.MainWindow
import Gesture.Database
import Gesture.HIDEmulation
from multiprocessing.pool import ThreadPool
import Bluetooth.Bluetooth

class MainWindow(QMainWindow, UI.MainWindow.Ui_MainWindow, QTableWidget):

    DropDownText=""
    values = None
    combo = list()

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
        self.values = Bluetooth.Bluetooth.Bluetooth().captureGesture()

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
        pool = ThreadPool(processes=1)
        async_result = pool.apply_async(listen)
        result_text = async_result.get()
        self.VoiceLabel.setText(result_text)

def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()