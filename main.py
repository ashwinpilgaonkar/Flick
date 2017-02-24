import sys
from PyQt5.QtWidgets import *
from Voice.SpeechRecognition import listen
from Voice.GoogleTTS import speak
from Voice.GoogleNewsParser import retrieveNews
import UI.MainWindow
import threading
from multiprocessing import Queue

class MainWindow(QMainWindow, UI.MainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.TalkButton.clicked.connect(self.TalkButton_OnClick)

    def TalkButton_OnClick(self):
        #Convert listened speech to text
        queue = Queue()
        text = ""
        self.VoiceLabel.setText("Listening...")
        listen_thread = threading.Thread(target=listen)
        listen_thread.start()

        #text = queue.get()
        #self.VoiceLabel.setText(text)

        #Speak recognized text (STT)
        if not listen_thread.is_alive():
            news = retrieveNews(text)
            speak(news)

def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()