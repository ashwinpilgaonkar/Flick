__author__ = 'priyanshubhatnagar'

import sys

from PyQt5.QtWidgets import *
from SpeechInteractionPage import *

class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        GridLayout = QGridLayout()
        self.setLayout(GridLayout)

        self.WidgetSpeech = SpeechInteractionPage()
        self.WidgetControl = QWidget()

        self.tabBar = QTabWidget()
        self.tabBar.addTab(self.WidgetControl,"Control Page")
        self.tabBar.addTab(self.WidgetSpeech,"Speech Interaction Page")

        #self.tabBar.currentChanged.connect(self.onTabChanged)

        GridLayout.addWidget(self.tabBar)

app = QApplication(sys.argv)

screen = MainWindow()
screen.show()

sys.exit(app.exec_())

