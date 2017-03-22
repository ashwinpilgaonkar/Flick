import sys
from PyQt5.QtWidgets import *
from Voice.SpeechRecognition import listen
import UI.MainWindow
import Gesture.Database
from multiprocessing.pool import ThreadPool
import pyautogui

class MainWindow(QMainWindow, UI.MainWindow.Ui_MainWindow, QTableWidget):

    DropDownText=""

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        #Initialize Gesture Page UI Elements
        self.ReadGestureButton.clicked.connect(self.ReadGestureButton_OnClick)
        self.CaptureGestureButton.clicked.connect(self.CaptureGestureButton_OnClick)
        self.AddButton.clicked.connect(self.AddButton_OnClick)
        self.ClearButton.clicked.connect(self.ClearButton_OnClick)
        self.SaveButton.clicked.connect(self.SaveButton_OnClick)
        self.FunctionDropdown.addItems(["A", "B", "C"])
        self.FunctionDropdown.currentIndexChanged.connect(self.Dropdown_OnChange)

        #initialize Voice Page UI Elements
        self.TalkButton.clicked.connect(self.TalkButton_OnClick)

    def ReadGestureButton_OnClick(self):
        print("Read Gesture")
        self.StatusLabel.setText("Reading...")

    def CaptureGestureButton_OnClick(self):
        print("Capture Gesture")
        self.StatusLabel.setText("Captured!")

    def AddButton_OnClick(self):

        dbOp = Gesture.Database.dbOperation()
        dbOp.create()
        count = dbOp.read()
        dbOp.insert(count+1, "ADS", "QWE")
        count = dbOp.read()
        dbOp.delete()

        dbOp.close()

        self.dbTable.setColumnCount(2)
        self.dbTable.setHeaderLabels(["Name", "Shortcut"])
        list = QTreeWidgetItem(["String A", "String B"])
        self.dbTable.addTopLevelItem(list)
        print("Add")

    def ClearButton_OnClick(self):

        print("Clear")

    def SaveButton_OnClick(self):
        pyautogui.keyDown('alt')
        pyautogui.keyDown('f4')
        print("Save")

    def Dropdown_OnChange(self):
        self.DropDownText=self.FunctionDropdown.currentText()

    def TalkButton_OnClick(self):
        #Convert listened speech to text
        self.VoiceLabel.setText("Listening...")
        pool = ThreadPool(processes=1)
        async_result = pool.apply_async(listen)
        result_text = async_result.get()
        pool.close()
        pool.join()
        self.VoiceLabel.setText(result_text)

def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()