import os # Взаємодія з операційною та файловою системою. Приклади застосування: запуск, створення файлів, отримання шляхів системи.
import sys # цей модуль надає доступ до деяких змінних, будемо застосовувати для роботи з додатком
import time # повертає час в секундах з початку епохи як число з плаваючею точкою
import json # робота з файлами де зберігаються дані (числа, строки (рядки), списки...) і обмін цими даними
import socket # використовуються для надсилання повідомлень через мережу. Модуль забезпечуює форму міжпроцесного зв'язку.
import base64 # кодує двійкові дані у друковані символи ASCII та декодує такі кодування назад у двійкові дані
import glob # Повертає список імен шляхів, які знаходяться в каталозі pythname
# import PIL
import pygame
import pyautogui # імітація дій користувача

from PyQt5 import (
        QtCore, # Дозволяє зареєструвати тип події. Метод повертає ідентифікатор зареєстрованої події.
        QtGui, # Компоненти графічного інтерфейсу (елементу управління), що грунтуються на візуальном поданні.                          
        QtWidgets # Модуль з бібліотеки "QT" з набором графічних "віджетів" (компонентів користувацького інтерфейсу) для створення додатків із графічним інтерфейсом.
    )
# from PyQt5.QtWidgets import QApplication
from des import * # Використовується для шифрування даних

# Створюємо клас(інструкцію) My_Thread
class My_Thread(QtCore.QThread):
    my_signal = QtCore.pyqtSignal(list)# Змінна що зберігає список сигналів
    # Створюємо метод конструктор, щоб описати характеристики класу
    def __init__(self, ip = None, port = None, parent = None):
        QtCore.QThread.__init__(self, parent) # сповіщаємо батьківському класу QtThread, про наявність точного такого параметра у класа нащадка
        #
        self.IP = ip # особиста адреса пристрою в інтернеті
        self.PORT = port # номер (ключ) по якому можна підключитись до серверу 
        self.ACTIVE_SOCKET = None # 
        self.COMMAND = "screen" # 
        #
        self.SERVER = socket.socket(
            socket.AF_INET, # застосовується для використання мережевих протоколів IPV-4
            socket.SOCK_STREAM # константа яка забезпечує стабільний зв'язок між сервером та клієнтом
        ) 
        self.SERVER.setsockopt(
            socket.SOL_SOCKET, # повертає значення, яке вказує, чи знаходиться сокет у режимі прослуховування 
            socket.SO_REUSEADDR, # допомагає функції bind здійснити підключення до IP та Port повторно 
            1
        ) #
        self.SERVER.bind((self.IP, self.PORT)) #
        self.SERVER.listen(1) # 
        
      
    # Метод, що приймає та обробляє дані
    def run(self):
        # Приймаємо вхідне з'єднання
        self.DATA_CONNECTION, ADDRESS = self.SERVER.accept()
        self.ACTIVE_SOCKET = self.DATA_CONNECTION

        while True:
            if self.COMMAND.split(" ")[0] != "screen":
                pass
            if self.COMMAND.split(" ")[0] == "screen":
                pass
    
    # Відправка даних клієнту
    def send_json(self, data):
        # обробляємо бінарні дані, з 0 та 1 переводимо до символьної строки
        try:
            json_data = json.dumps(data.decode("utf-8"))
        except:
            json_data = json.dumps(data)
        # у випадку, якщо клієнт розірве з'єднання, але сервер все ще відправляє команди
        try:
            self.ACTIVE_SOCKET.send(json_data.encode('utf-8'))
        except ConnectionResetError:
            # переводимо ACTIVE_SOCKET в початковий стан, з'єднання розірвано
            self.ACTIVE_SOCKET = None    
    
    # отримуємо дані від користувача та зберігаємо їх у json файлах
    def receive_json(self):
        json_data = ""
        while True:
            try:
                # якщо є з'єднання з клієнтом
                if self.ACTIVE_SOCKET != None:
                    # Отримувати дані від кліента та декодувати їх зберігаючи у json файлі
                    json_data += self.ACTIVE_SOCKET.recv(1024).decode('utf-8')
                    # json_data = json_data + self.ACTIVE_SOCKET.recv(1024).decode('utf-8')
            except ValueError:
                pass   
                 
# умова __name__  == '__main__' виконує код що написаний нижче тільки в модулі server.py
if __name__  == '__main__':
    # Вказуються висота та ширина вікна та зображення.
    WIN_WIDTH, WIN_HEIGHT = 1300, 800
    FILE_IMAGE = "2.png"
    #
    file_name = "1.jpg"
    #
    text_except = ''
    #
    try:
        file_image = pygame.image.load(FILE_IMAGE)
    except:
        # Завантажуємо зображення з папки до програми
        try:
            file_image = pygame.image.load(file_name)
            # Змінюємо розміри зображення
            file_image = pygame.transform.scale(file_image, (WIN_WIDTH, WIN_HEIGHT))
            # зберігаємо редаговане зображення в папці проекту
            pygame.image.save(file_image, "2.png")
        except:
            text_except = "image doesnt exist"
    # if not os.path.exists('2.png'):
    # if not os.path.isfile('2.png'):
        # print(1)
        # file_image = pygame.image.load(file_name)
        # file_image = pygame.transform.scale(file_image, (WIN_WIDTH, WIN_HEIGHT))
        # pygame.image.save(file_image, "2.png")
    # створюємо додаток my_app
    my_app = QtWidgets.QApplication(sys.argv)
    # створюємо вікно додатку
    app_window = QtWidgets.QWidget()
    # задаємо розміри  вікна додатку
    app_window.setFixedSize(WIN_WIDTH, WIN_HEIGHT)
    # Відповідає за створення об'єкта (текст) який буде відображений на екрані в додатку 
    text = QtWidgets.QLabel(text_except)
    # Створюємо об'єкт вертикального layout, на якому будемо розміщувати текст
    vertical_layout = QtWidgets.QVBoxLayout()
    # додаемо текст до вертекального лейауту
    vertical_layout.addWidget(text)
    # встановлюємо вертикальний layout до вікна додатку
    app_window.setLayout(vertical_layout)
    # налаштовуємо: колір фону, та картинку фону додатку 
    app_window.setStyleSheet(
        f'''
            background-color: rgb(80,80,80);
            background-image: url({FILE_IMAGE});
            background-repeat: no-repeat;
        ''' 
    )
    #
    text.setStyleSheet(
        '''
            font-size: 100px;
            qproperty-alignment: "AlignCenter";
            color: red;
        '''
    )
    # Задаємо ім'я додатку 
    app_window.setWindowTitle("Вікно додатка")
    # Відображає вікно додатка
    app_window.show()
    # Робе так щоб вікно не закривалось вікно додатку
    my_app.exec_()
    

    
