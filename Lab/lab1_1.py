#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QTextEdit, QAction, QApplication, QMessageBox,
                             QHBoxLayout, QVBoxLayout, QPushButton, QGridLayout, QLabel, QDesktopWidget, QLineEdit)
from PyQt5.QtGui import QIcon


class Box(QWidget):

    def __init__(self):
        super().__init__()
        self.textEdit = QTextEdit()
        self.nameFile = QLineEdit()

        self.initUI()

    # Всплывающее окно успешного выполнения
    def message(self):
        msgBox = QMessageBox()
        msgBox.setText("Действие успешно выполнено.")
        msgBox.exec_()

    # Сохранение текста
    def save_text(self):
        with open('privat/' + self.nameFile.displayText() + '.txt', 'w') as f:
            my_text = self.textEdit.toPlainText()
            f.write(my_text)
        self.message()

    # Копирование текста
    def copy_text(self):
        with open('privat/' + self.nameFile.displayText() + '.txt', 'r') as f:
            my_text = f.read()
            with open('public/' + self.nameFile.displayText() + '.txt', 'w') as file:
                file.write(my_text)
        self.message()

    def initUI(self):
        text = QLabel('Введите текст:')
        name = QLabel('Введите имя файла:')

        okButton = QPushButton("Сохранить в приватную папку")
        copyButton = QPushButton("Переместить из приватной папки в публичную")

        hbox = QHBoxLayout()

        hbox.addWidget(okButton)
        hbox.addWidget(copyButton)

        grid = QGridLayout()
        grid.setSpacing(5)
        grid.addWidget(name, 0, 0)
        grid.addWidget(self.nameFile, 1, 0, 1, 2)
        grid.addWidget(text, 2, 0)
        grid.addWidget(self.textEdit, 3, 0, 3, 2)
        grid.addLayout(hbox, 6, 0)

        self.setLayout(grid)

        okButton.clicked.connect(self.save_text)
        copyButton.clicked.connect(self.copy_text)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Buttons')
        self.show()


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        okButton = QPushButton("OK", self)
        cancelButton = QPushButton("Cancel", self)

        exitAction = QAction(QIcon('Icon/exit.png'), '&Выйти', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Закрыть приложение')
        exitAction.triggered.connect(self.close)

        self.statusBar()

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('&Действие')
        fileMenu.addAction(exitAction)

        toolbar = self.addToolBar('Выйти')
        toolbar.addAction(exitAction)

        widget = Box()
        self.setCentralWidget(widget)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Lab1')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
