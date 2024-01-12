import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QCalendarWidget, \
    QListWidget, QMessageBox, QLineEdit, QTimeEdit, QDateTimeEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDateTime, QTimer
from plyer import notification

class CalendarApp(QWidget):
    def __init__(self):
        super().__init__()

        self.notes = []

        self.init_ui()

        # Таймер для перевірки часу і виведення повідомлення
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_notes)
        self.timer.start(1000)  # Кожну секунду

    def init_ui(self):
        layout = QVBoxLayout()

        # Календар
        self.cal = QCalendarWidget()
        layout.addWidget(self.cal)

        # Поле для введення назви нотатки
        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText("Введіть назву нотатки")
        layout.addWidget(self.title_input)

        # Поле для введення опису нотатки
        self.description_input = QLineEdit(self)
        self.description_input.setPlaceholderText("Введіть опис нотатки")
        layout.addWidget(self.description_input)

        # Вибір часу для нотатки
        self.time_input = QTimeEdit(self)
        layout.addWidget(self.time_input)

        # Кнопка для додавання нотатки
        add_button = QPushButton("Додати нотатку", self)
        add_button.clicked.connect(self.add_note)
        layout.addWidget(add_button)

        # Список нотаток
        self.note_list = QListWidget(self)
        layout.addWidget(self.note_list)

        # Кнопка для видалення нотатки
        remove_button = QPushButton("Видалити нотатку", self)
        remove_button.clicked.connect(self.remove_note)
        layout.addWidget(remove_button)

        self.setLayout(layout)
        self.setWindowTitle('Календар та Нотатки')
        self.show()

    def add_note(self):
        selected_date = self.cal.selectedDate()
        note_title = self.title_input.text()
        note_description = self.description_input.text()
        note_time = self.time_input.time()

        if note_title and note_time.isValid():
            note_datetime = QDateTime(selected_date, note_time)
            self.notes.append({
                "title": note_title,
                "description": note_description,
                "datetime": note_datetime
            })

            QMessageBox.information(self, "Успіх", f"Нотатка '{note_title}' додана успішно!")

            self.update_note_list()

    def remove_note(self, index):
        del self.notes[index]
        self.update_note_list()

    def update_note_list(self):
        self.note_list.clear()

        for index, note in enumerate(self.notes):
            formatted_note = f"{note['title']} ({note['datetime'].toString('dd/MM/yyyy hh:mm')})"
            self.note_list.addItem(formatted_note)

    def check_notes(self):
        current_datetime = QDateTime.currentDateTime()

        for index, note in enumerate(self.notes):
            note_datetime = note['datetime']
            if current_datetime >= note_datetime:
                notification_title = f"Повідомлення: {note['title']}"
                notification_message = f"{note['description']}"
                self.show_notification(notification_title, notification_message)
                self.remove_note(index)

    def show_notification(self, title, message):
        notification.notify(
            title=title,
            message=message,
            app_icon=None,
            timeout=10
        )


# if __name__ == '__main__':
#     app = QApplication([])
#     window = CalendarApp()
#     sys.exit(app.exec_())
