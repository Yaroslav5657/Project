import ctypes
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QPushButton, QDialog, QGraphicsOpacityEffect, QFileDialog, QTextEdit
from PyQt5.QtCore import Qt
from timer_app import TimerApp
from notes_app import CalendarApp
from off_pc_app import ShutdownApp
import sys
from F_site  import MainWindow, AddWebsiteDialog
from F_site import MainWindow as WebsiteMainWindow, AddWebsiteDialog


class FancyButton(QPushButton):
    def __init__(self, text, parent=None):
        super(FancyButton, self).__init__(text, parent)

        # Дополнительный стиль для кнопок
        self.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                transition-duration: 0.4s;
                cursor: pointer;
                border-radius: 8px;
            }

            QPushButton:hover {
                background-color: white;
                color: black;
            }
        """)

        # Дополнительная анимация для нажатия кнопок
        self.animation = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.animation)
        self.clicked.connect(self.on_click)

    def on_click(self):
        # Анимация для нажатия
        self.animation.setOpacity(0.5)


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)

        self.setWindowTitle("Настройки")
        self.setGeometry(200, 200, 300, 150)

        self.theme_combobox = QComboBox(self)
        self.theme_combobox.addItems(["Светлая тема", "Темная тема"])

        self.apply_button = QPushButton("Изменить тему", self)
        self.apply_button.clicked.connect(self.apply_theme)

        layout = QVBoxLayout()
        layout.addWidget(self.theme_combobox)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)

    def apply_theme(self):
        # Применяем выбранную тему из окна настроек
        theme_index = self.theme_combobox.currentIndex()
        if theme_index == 0:  # Светлая тема
            self.parent().setStyleSheet("")
        elif theme_index == 1:  # Темная тема
            self.parent().setStyleSheet("QMainWindow { background-color: #333; color: white; }")

        # Закрываем окно настроек
        self.accept()


class DesktopApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TimeNotes Calendar")

        # Добавим FancyButton для кнопок "Таймер" и "Нотатки"
        self.timer_button = FancyButton("Таймер", self)
        self.notes_button = FancyButton("Нотатки", self)
        self.settings_button = FancyButton("Настройки", self)
        self.shutdown_button = FancyButton("Выключить компьютер", self)
        self.favorite_website_button = FancyButton("Улюблений сайт", self)

        # Расположим кнопки в вертикальном layout
        layout = QVBoxLayout()
        layout.addWidget(self.timer_button)
        layout.addWidget(self.notes_button)
        layout.addWidget(self.settings_button)
        layout.addWidget(self.shutdown_button)
        layout.addWidget(self.favorite_website_button)
        layout.addStretch()  # Добавим растягивающееся пространство

        # Создаем виджет и устанавливаем его в центральную область главного окна
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Назначаем действия для кнопок
        self.timer_button.clicked.connect(self.open_timer)
        self.notes_button.clicked.connect(self.open_notes)
        self.settings_button.clicked.connect(self.open_settings)
        self.shutdown_button.clicked.connect(self.open_shutdown)
        self.favorite_website_button.clicked.connect(self.open_favorite_website)

        # Ініціалізуємо об'єкт для виключення комп'ютера
        self.shutdown_app = ShutdownApp()

    def open_timer(self):
        self.timer_app = TimerApp()
        self.timer_app.show()

    def open_notes(self):
        if not hasattr(self, 'notes_window') or not self.notes_window.isVisible():
            self.notes_window = CalendarApp()
            self.notes_window.show()

    def open_settings(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec_()

    def open_shutdown(self):
        self.shutdown_app.show()
        
    def open_favorite_website(self):
        self.website_window = WebsiteMainWindow()
        self.website_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = DesktopApp()
    main_window.setGeometry(100, 100, 1000, 400)
    main_window.show()
    sys.exit(app.exec_())