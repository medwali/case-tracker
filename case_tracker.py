import sys
import sqlite3
from datetime import datetime, timedelta
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import QTimer

class CaseTimer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initDB()
        self.current_case_id = None
        self.updateAverageDuration()

    def initUI(self):
        self.setWindowTitle('Case Tracker')
        self.setGeometry(100, 100, 200, 150)

        self.layout = QVBoxLayout()

        self.label = QLabel('00:00:00')
        self.layout.addWidget(self.label)

        self.avgLabel = QLabel('Average Duration: 00:00:00')
        self.layout.addWidget(self.avgLabel)

        self.startCaseButton = QPushButton('Start Case')
        self.startCaseButton.clicked.connect(self.startCase)
        self.layout.addWidget(self.startCaseButton)

        self.stopCaseButton = QPushButton('Stop Case')
        self.stopCaseButton.clicked.connect(self.stopCase)
        self.layout.addWidget(self.stopCaseButton)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)

        self.counter = 0

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.updateButtons(False)

    def initDB(self):
        self.conn = sqlite3.connect('case_timer.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_date TEXT,
                start_time TEXT,
                end_time TEXT
            )
        ''')
        self.conn.commit()

    def startCase(self):
        self.timer.start(1000)
        self.updateButtons(True)
        current_datetime = datetime.now()
        date_str = current_datetime.strftime('%Y-%m-%d')
        time_str = current_datetime.strftime('%H:%M:%S')
        self.cursor.execute("INSERT INTO cases (case_date, start_time) VALUES (?, ?)", (date_str, time_str))
        self.conn.commit()
        self.current_case_id = self.cursor.lastrowid

    def stopCase(self):
        self.timer.stop()
        end_time_str = datetime.now().strftime('%H:%M:%S')
        if self.current_case_id is not None:
            self.cursor.execute("UPDATE cases SET end_time = ? WHERE id = ?", (end_time_str, self.current_case_id))
            self.conn.commit()
        self.updateAverageDuration()
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

    def updateAverageDuration(self):
        last_monday = datetime.now() - timedelta(days=datetime.now().weekday())
        last_monday_str = last_monday.strftime('%Y-%m-%d')
        self.cursor.execute("""
            SELECT AVG(strftime('%s', end_time) - strftime('%s', start_time)) 
            FROM cases 
            WHERE date(case_date) >= date(?) AND end_time IS NOT NULL
        """, (last_monday_str,))
        avg_seconds = self.cursor.fetchone()[0]
        if avg_seconds is not None:
            hours, remainder = divmod(int(avg_seconds), 3600)
            minutes, seconds = divmod(remainder, 60)
            avg_duration_str = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
            self.avgLabel.setText(f'Average Duration: {avg_duration_str}')
        else:
            self.avgLabel.setText('Average Duration: 00:00:00')

def main():
    app = QApplication(sys.argv)
    ex = CaseTimer()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

