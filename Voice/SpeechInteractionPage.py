from PyQt5.QtWidgets import *
from Voice.SpeechRecognition import listen
from Voice.GoogleSTT import Googlelisten
from Voice.GoogleTTS import speak
from Voice.GoogleNewsParser import retrieveNews
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
        #text = Googlelisten()
        text = ""
        text = listen()
        self.label.setText(text)
        news = retrieveNews(text)
        speak(news)