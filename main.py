import sys
from PyQt5.QtWidgets import *
from Voice.SpeechRecognition import listen
import UI.MainWindow
import threading

class MainWindow(QMainWindow, UI.MainWindow.Ui_MainWindow):

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
        print("Add")

    def ClearButton_OnClick(self):
        print("Clear")

    def SaveButton_OnClick(self):
        print("Save")

    def Dropdown_OnChange(self):
        self.DropDownText=self.FunctionDropdown.currentText()

    def TalkButton_OnClick(self):
        #Convert listened speech to text
        self.VoiceLabel.setText("Listening...")
        listen_thread = threading.Thread(target=listen,args=self.VoiceLabel)
        listen_thread.start()


def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()