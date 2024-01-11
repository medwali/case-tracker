import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import QTimer

class Stopwatch(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Case Timer')
        self.setGeometry(100, 100, 200, 100)

        self.layout = QVBoxLayout()

        self.label = QLabel('00:00:00')
        self.layout.addWidget(self.label)

        self.startCaseButton = QPushButton('Start Case')
        self.startCaseButton.clicked.connect(self.startTimer)
        self.layout.addWidget(self.startCaseButton)

        self.stopCaseButton = QPushButton('Stop Case')
        self.stopCaseButton.clicked.connect(self.resetTimer)
        self.layout.addWidget(self.stopCaseButton)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)

        self.counter = 0

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.updateButtons(False)

    def startTimer(self):
        self.timer.start(1000)
        self.updateButtons(True)

    def resetTimer(self):
        self.timer.stop()
        self.counter = 0
        self.label.setText('00:00:00')
        self.updateButtons(False)

    def updateTime(self):
        self.counter += 1
        time_str = f'{self.counter // 3600:02d}:{(self.counter // 60) % 60:02d}:{self.counter % 60:02d}'
        self.label.setText(time_str)

    def updateButtons(self, isRunning):
        self.startCaseButton.setEnabled(not isRunning)
        self.stopCaseButton.setEnabled(isRunning)

def main():
    app = QApplication(sys.argv)
    ex = Stopwatch()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

