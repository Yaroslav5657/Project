import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, \
    QLCDNumber, QGridLayout, QSpinBox, QAbstractSpinBox
from PyQt5.QtCore import QTimer, Qt
from plyer import notification

class TimerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.lcd = QLCDNumber()
        self.button = QPushButton("Start")
        self.button.clicked.connect(self.timerStart)
        self.buttonReset = QPushButton("Стоп")
        self.buttonReset.clicked.connect(self.timerStop) 
        self.buttonResetToZero = QPushButton("Скинути")
        self.buttonResetToZero.clicked.connect(self.resetTimerToZero)
        self.spinBox = QSpinBox()
        self.spinBox.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinBox.setMaximum(1000)
        self.spinBox.setSingleStep(1)
        self.spinBox.setProperty("value", 7)
        self.spinBox.setWrapping(True)
        self.spinBox.setAlignment(Qt.AlignRight)

        layout = QGridLayout()
        layout.addWidget(self.lcd, 0, 0, 1, 3)
        layout.addWidget(self.spinBox, 1, 0, 1, 3)
        layout.addWidget(self.button, 2, 0)
        layout.addWidget(self.buttonReset, 2, 1)
        layout.addWidget(self.buttonResetToZero, 2, 2)
        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.setInterval(1000)
        self.time = 0

    def showTime(self):
        self.lcd.display(self.time)
        self.time -= 1
        if self.time == 0:
            self.timer.stop()
            self.button.setText("Start")
            self.show_notification("Час закінчився")

    def timerStart(self):
        if self.button.text() == "Start":
            if not self.time:
                self.time = self.spinBox.value()
            self.timer.start()
            self.button.setText("Stop")
        else:
            self.timer.stop()
            self.button.setText("Start")

    def timerStop(self):  
        self.timer.stop()
        self.button.setText("Start")

    def resetTimerToZero(self):
        self.timer.stop()
        self.button.setText("Start")
        self.time = 0
        self.lcd.display(self.time)

    def show_notification(self, message):
        notification.notify(
            title='Timer Notification',
            message=message,
            app_icon=None,
            timeout=10
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    timerApp = TimerApp()
    timerApp.resize(300, 150)
    timerApp.show()
    sys.exit(app.exec())
