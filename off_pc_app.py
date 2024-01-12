import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QTimeEdit, QPushButton
from PyQt5.QtCore import QTimer, QTime
from datetime import datetime, timedelta
from plyer import notification
import subprocess


class ShutdownApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Scheduled Shutdown')
        self.setGeometry(300, 300, 300, 200)

        self.time_label = QLabel('Виберіть час для виключення комп\'ютера:')
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat('HH:mm:ss')
        self.time_edit.setTime(QTime.currentTime())

        self.shutdown_btn = QPushButton('Запланувати виключення')
        self.shutdown_btn.clicked.connect(self.schedule_shutdown)

        layout = QVBoxLayout()
        layout.addWidget(self.time_label)
        layout.addWidget(self.time_edit)
        layout.addWidget(self.shutdown_btn)

        self.setLayout(layout)

    def schedule_shutdown(self):
        selected_time = self.time_edit.time()

        current_datetime = datetime.now()
        selected_datetime = datetime(current_datetime.year, current_datetime.month, current_datetime.day,
                                      selected_time.hour(), selected_time.minute(), selected_time.second())

        time_difference = selected_datetime - current_datetime

        notification.notify(
            title='Scheduled Shutdown',
            message=f'Комп\'ютер буде виключено через {time_difference}',
            app_icon=None,
            timeout=10,
        )

        self.start_timer(int(time_difference.total_seconds() - 1800), self.show_notification,
                         'Залишилося 30 хвилин до виключення')
        self.start_timer(int(time_difference.total_seconds() - 60), self.show_notification, 'Залишилося 1 хвилина до виключення')
        self.start_timer(int(time_difference.total_seconds()), self.shutdown_computer)

        # Закриття вікна після натискання кнопки вимкнення комп'ютера
        self.close()

    def start_timer(self, seconds, callback, message=None):
        timer = QTimer(self)
        timer.timeout.connect(lambda: callback(message) if message else callback())
        timer.start(seconds * 1000)

    def show_notification(self, message):
        notification.notify(
            title='Scheduled Shutdown',
            message=message,
            app_icon=None,
            timeout=10,
        )

    def shutdown_computer(self):
        subprocess.run(['shutdown', '/s', '/t', '1'])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ShutdownApp()
    window.show()
    sys.exit(app.exec_())
