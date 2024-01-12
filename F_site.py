import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QDialog, QLabel, QLineEdit, QHBoxLayout, QMessageBox
import webbrowser

class WebsiteManager:
    def __init__(self):
        self.websites = []
        self.load_from_file()

    def add_website(self, title, url):
        self.websites.append({'title': title, 'url': url})
        self.save_to_file()

    def remove_website(self, title):
        self.websites = [site for site in self.websites if site['title'] != title]
        self.save_to_file()

    def load_from_file(self):
        try:
            with open('sites.txt', 'r') as file:
                for line in file:
                    title, url = line.strip().split('|')
                    self.add_website(title.strip(), url.strip())
        except FileNotFoundError:
            pass

    def save_to_file(self):
        try:
            with open('sites.txt', 'w') as file:
                for website in self.websites:
                    file.write(f"{website['title']} | {website['url']}\n")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Не вдалося зберегти: {e}")

class AddWebsiteDialog(QDialog):
    def __init__(self, website_manager):
        super().__init__()

        self.website_manager = website_manager

        self.setWindowTitle("Додати веб-сайт")
        self.setGeometry(200, 200, 400, 150)

        self.title_label = QLabel("Назва:")
        self.title_input = QLineEdit()

        self.url_label = QLabel("URL:")
        self.url_input = QLineEdit()

        self.add_button = QPushButton("Додати")
        self.add_button.clicked.connect(self.add_website)

        layout = QVBoxLayout()
        form_layout = QVBoxLayout()
        form_layout.addWidget(self.title_label)
        form_layout.addWidget(self.title_input)
        form_layout.addWidget(self.url_label)
        form_layout.addWidget(self.url_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def add_website(self):
        title = self.title_input.text()
        url = self.url_input.text()

        if title and url:
            self.website_manager.add_website(title, url)
            self.accept()
        else:
            QMessageBox.warning(self, "Увага", "Заголовок і URL обов'язкові!")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Website Manager")
        self.setGeometry(100, 100, 600, 400)

        self.website_manager = WebsiteManager()

        self.add_button = QPushButton("Додати веб-сайт")
        self.add_button.clicked.connect(self.show_add_website_dialog)

        self.website_buttons_layout = QVBoxLayout()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.add_button)
        main_layout.addLayout(self.website_buttons_layout)

        self.setLayout(main_layout)

        self.update_website_buttons()

    def show_add_website_dialog(self):
        dialog = AddWebsiteDialog(self.website_manager)
        if dialog.exec_() == QDialog.Accepted:
            self.update_website_buttons()

    def show_website_options_dialog(self, title):
        options_dialog = QDialog(self)
        options_dialog.setWindowTitle(title)
        options_dialog.setGeometry(300, 300, 300, 100)

        delete_button = QPushButton("Видалити веб-сайт")
        delete_button.clicked.connect(lambda: self.delete_website(title))

        open_button = QPushButton("Відкрити веб-сайт")
        open_button.clicked.connect(lambda: self.open_website(title))

        layout = QHBoxLayout()
        layout.addWidget(delete_button)
        layout.addWidget(open_button)

        options_dialog.setLayout(layout)

        options_dialog.exec_()

    def delete_website(self, title):
        self.website_manager.remove_website(title)
        self.update_website_buttons()

    def open_website(self, title):
        website = next(site for site in self.website_manager.websites if site['title'] == title)
        webbrowser.open(website['url'])

    def update_website_buttons(self):
        for i in reversed(range(self.website_buttons_layout.count())):
            self.website_buttons_layout.itemAt(i).widget().setParent(None)

        for website in self.website_manager.websites:
            button = FancyButton(website['title'])
            button.clicked.connect(lambda _, title=website['title']: self.show_website_options_dialog(title))
            self.website_buttons_layout.addWidget(button)

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

        # # Дополнительная анимация для нажатия кнопок
        # self.animation = QGraphicsOpacityEffect(self)
        # self.setGraphicsEffect(self.animation)
        # self.clicked.connect(self.on_click)

    def on_click(self):
        # Анимация для нажатия
        self.animation.setOpacity(0.5)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())