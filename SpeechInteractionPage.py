__author__ = 'priyanshubhatnagar'

from PyQt5.QtWidgets import *
from Flick.SpeechRecognition import listen
from Flick.GoogleSTT import Googlelisten
from Flick.GoogleTTS import speak
import sys

class SpeechInteractionPage(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        GridLayout = QGridLayout()
        self.setLayout(GridLayout)

        button = QPushButton("Talk")
        button.setFixedHeight(70)
        button.setFixedWidth(70)
        button.clicked.connect(self.on_button_clicked)

        self.label = QLabel("Hi this is Speech Grid")

        GridLayout.addWidget(self.label, 0, 1)
        GridLayout.addWidget(button, 0, 0)

    def on_button_clicked(self):
        text = ""
        text = listen()
        #text = Googlelisten()
        self.label.setText(text)
        speak(text)
