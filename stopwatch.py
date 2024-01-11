import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import QTimer

class Stopwatch(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Stopwatch')
        self.setGeometry(100, 100, 200, 100)

        self.layout = QVBoxLayout()

        self.label = QLabel('00:00:00')
        self.layout.addWidget(self.label)

        self.startButton = QPushButton('Start')
        self.startButton.clicked.connect(self.startTimer)
        self.layout.addWidget(self.startButton)

        self.stopButton = QPushButton('Stop')
        self.stopButton.clicked.connect(self.stopTimer)
        self.layout.addWidget(self.stopButton)

        self.resetButton = QPushButton('Reset')
        self.resetButton.clicked.connect(self.resetTimer)
        self.layout.addWidget(self.resetButton)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)

        self.counter = 0

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def startTimer(self):
        self.timer.start(1000)
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)

    def stopTimer(self):
        self.timer.stop()
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)

    def resetTimer(self):
        self.timer.stop()
        self.counter = 0
        self.label.setText('00:00:00')
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)

    def updateTime(self):
        self.counter += 1
        time_str = f'{self.counter // 3600:02d}:{(self.counter // 60) % 60:02d}:{self.counter % 60:02d}'
        self.label.setText(time_str)

def main():
    app = QApplication(sys.argv)
    ex = Stopwatch()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

