from PyQt6 import QtCore, QtGui, QtWidgets
import time
import threading
from pynput.mouse import Button, Controller
from pynput import keyboard


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
# Создание переменных, флагов для потоков и вызов функций
        self.mouse = Controller()
        self.keyboard = Controller()

        self.clicking = False
        self.click_thread = None
        self.hotkey = keyboard.Key.f10

        self.init_ui()
        self.start_or_stop()

        self.listener_thread = threading.Thread(target=self.clicking_listener, daemon=True)
        self.listener_thread.start()

    def init_ui(self):
# Создание окна автокликера
        self.setObjectName("MainWindow")
        self.setWindowTitle("Autoclicker")
        self.resize(300, 200)
        self.setStyleSheet("background-color: rgb(199, 199, 199);")

        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
# Создание текстого поля "Autoclicker"
        self.label_Autoclicker = QtWidgets.QLabel("Autoclicker", self.centralwidget)
        self.label_Autoclicker.setGeometry(0, 0, 150, 50)
        self.label_Autoclicker.setStyleSheet("font: 18pt \"Calibri\";")
        self.label_Autoclicker.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
# Создание кнопки "START"
        self.btn_start = QtWidgets.QPushButton("START", self.centralwidget)
        self.btn_start.setGeometry(20, 80, 100, 30)
        self.btn_start.setStyleSheet("font: 15pt \"Calibri\";")
# Создание кнопки "STOP"
        self.btn_stop = QtWidgets.QPushButton("STOP", self.centralwidget)
        self.btn_stop.setGeometry(20, 140, 100, 30)
        self.btn_stop.setStyleSheet("font: 15pt \"Calibri\";")
# Создание текстого поля для отображения статуса кликера
        self.label_statustext = QtWidgets.QLabel("Status", self.centralwidget)
        self.label_statustext.setGeometry(200, 0, 100, 50)
        self.label_statustext.setStyleSheet(
            "background-color: rgb(84, 84, 84); font: 18pt \"Calibri\"; color: rgb(255, 255, 255);")
        self.label_statustext.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_status = QtWidgets.QLabel("None", self.centralwidget)
        self.label_status.setGeometry(200, 50, 100, 30)
        self.label_status.setStyleSheet(
            "background-color: rgb(84, 84, 84); font: 15pt \"Calibri\"; color: rgb(255, 0, 0);")
        self.label_status.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
# Создание текстого поля для горячих клавиш
        self.label_hotkey = QtWidgets.QLabel("Hotkey", self.centralwidget)
        self.label_hotkey.setGeometry(175, 130, 125, 20)
        self.label_hotkey.setStyleSheet("background-color: rgb(255, 255, 255); font: 12pt \"Calibri\";")
        self.label_hotkey_data = QtWidgets.QLabel("f10", self.centralwidget)
        self.label_hotkey_data.setGeometry(175, 150, 125, 22)
        self.label_hotkey_data.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label_hotkey_data.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
# Создание функции для кнопок "START" и "STOP"
    def start_or_stop(self):
        self.btn_start.clicked.connect(self.start_clicking)
        self.btn_stop.clicked.connect(self.stop_clicking)
# Создание функции запуска кликера
    def start_clicking(self):
        self.label_status.setText(self.btn_start.text())
        if self.click_thread is None or not self.click_thread.is_alive():
            self.clicking = True
            self.click_thread = threading.Thread(target=self.clicker, daemon=True)
            self.click_thread.start()
# Создание функции остановки кликера
    def stop_clicking(self):
        self.label_status.setText(self.btn_stop.text())
        self.clicking = False
# Создание функции кликера
    def clicker(self):
        while self.clicking:
            self.mouse.click(Button.left, 1)
            time.sleep(0.01)
# Создание функции отдельного потока кликера
    def clicking_listener(self):
        with keyboard.Listener(on_press=self.on_key_press) as listener:
            listener.join()
    def on_key_press(self, key):
        if self.clicking and key == self.hotkey:
            self.stop_clicking()
        elif not self.clicking and key == self.hotkey:
            self.start_clicking()
# Запуск приложения
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
