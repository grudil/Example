from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize, Qt, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem, QLabel, \
    QLineEdit, QCheckBox, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QBoxLayout
import json

# Класс главной таблицы
class GenerTable(object):
    def __init__(self):
        self.alphabet = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz,."
        self.name = []

    def check_file(self):
        path = "matrix.json"

        with open(path, 'r') as f:
            data = json.load(f)
            self.list = data
            for name in data:
                self.name.append(name)

    # Добавление пользователей из матрицы
    def add_test(self, nameUser):
        path = "matrix.json"

        with open(path, 'r') as f:
            data = json.load(f)
            data[nameUser] = []
            for i in range(56):
                data[nameUser].append(0)
            with open(path, 'w') as f:
                json.dump(data, f)

    # Изменение матрицы в файле при измении чекбокса
    def exchange_test(self, fromInd, toInd):
        countRow = 0
        countCol = 0
        path = "matrix.json"
        tmp = []

        with open(path, 'r') as f:
            data = json.load(f)
            for nameFrom in data:
                if countRow == fromInd:
                    print(nameFrom)
                    dataFrom = data[nameFrom]
                    for nameTo in data:
                        if countCol == toInd:
                            dataTo = data[nameTo]
                            for j in range(len(dataTo)):
                                if dataFrom[j] != dataTo[j]:
                                    if dataFrom[j]:
                                        dataTo[j] = 1

                            print(nameTo)
                            #data[nameFrom] = data[nameTo]
                            data[nameTo] = dataTo

                        countCol += 1
                    with open(path, 'w') as f:
                        json.dump(data, f)

                countRow += 1

    # Удаление пользователя из матрицы в файле
    def delete_test(self, nameUser):
        path = "matrix.json"

        with open(path, 'r') as f:
            data = json.load(f)
            del data[nameUser]
            with open(path, 'w') as f:
                json.dump(data, f)

    # Изменение матрицы в файле при отключении чекбоксов
    def disable_state(self, row, col):
        count = 0
        path = "matrix.json"
        with open(path, 'r') as f:
            data = json.load(f)
            for name in data:
                if count == row:
                    data[name][col] = 0
                    with open(path, 'w') as f:
                        json.dump(data, f)
                    #print(name)
                count += 1

    # Изменение матрицы в файле при включении чекбоксов
    def enable_state(self, row, col):
        count = 0
        path = "matrix.json"

        with open(path, 'r') as f:
            data = json.load(f)
            for name in data:
                if count == row:
                    data[name][col] = 1
                    with open(path, 'w') as f:
                        json.dump(data, f)
                    #print(name)
                count += 1

    # Проверка введеного текста на допустимые символы
    def verificate_text(self, nameUser, text):
        count = 0
        path = "matrix.json"
        alpha = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz,."
        outText = ''

        with open(path, 'r') as f:
            data = json.load(f)
            verifAlpha = []
            for sym in data[nameUser]:
                if sym:
                    verifAlpha.append(alpha[count])
                count += 1

        for sym in text:
            if sym in verifAlpha:
                outText += sym

        return outText


class Ui_MainWindow(object):

    # Рекция при активировании чекбокса
    def activeCheckBox(self):

        a = GenerTable()
        a.check_file()
        sender = self.MainWindow.sender()

        item = (self.table.cellWidget(sender.currentRow(), sender.currentColumn()))
        self.checkB = item.layout().itemAt(0).widget()

        self.currentRow = sender.currentRow()
        self.currentColmn = sender.currentColumn()

        if self.checkB.isChecked():
            self.checkB.setChecked(0)
            a.disable_state(self.currentRow, self.currentColmn)
        else:
            self.checkB.setChecked(1)
            a.enable_state(self.currentRow, self.currentColmn)

        if self.checkB.isChecked():
            print(self.currentRow, self.currentColmn)
        else:
            print(self.currentRow, self.currentColmn)

    # Добавление нового пользователя
    def add_user(self):
        a = GenerTable()
        a.add_test(self.createLineEdit.text())
        a.check_file()
        alph = list(a.alphabet[:])
        self.table.setRowCount(len(a.name))
        self.table.setVerticalHeaderLabels(a.name)
        self.removeComboBox.addItem(a.name[len(a.name) - 1])
        self.grantToComboBox.addItem(a.name[len(a.name) - 1])
        self.grantFromComboBox.addItem(a.name[len(a.name) - 1])
        self.userComboBox.addItem(a.name[len(a.name) - 1])

        if self.linEditAlph.text():
            for sym in self.linEditAlph.text():
                if sym not in alph:
                    alph.append(sym)
                    a.alphabet+=str(sym)

        for row in range(len(a.name)):
            for col in range(len(alph)):
                chkBoxWidget = QWidget()
                self.chkBox = QCheckBox()

                layoutCheckBox = QHBoxLayout(chkBoxWidget)
                layoutCheckBox.addWidget(self.chkBox)
                layoutCheckBox.setAlignment(Qt.AlignLeft)
                layoutCheckBox.setContentsMargins(0, 0, 0, 0)
                if a.list[a.name[row]][col]:
                    self.chkBox.setChecked(1)
                else:
                    self.chkBox.setChecked(0)

                self.table.setCellWidget(row, col, chkBoxWidget)

    # Удаление пользователя
    def delete_user(self, index):
        print(index)
        a = GenerTable()
        a.delete_test(self.removeComboBox.currentText())
        self.removeComboBox.removeItem(index)
        self.grantToComboBox.removeItem(index)
        self.grantFromComboBox.removeItem(index)
        self.userComboBox.removeItem(index)
        a.check_file()
        self.table.setRowCount(len(a.name))
        self.table.setVerticalHeaderLabels(a.name)

    # Удаление пользователя из чекбокса
    def test(self):
        self.delete_user(self.removeComboBox.currentIndex())

    # Изменение чекбокса
    def exchange(self):
        a = GenerTable()
        a.check_file()
        alph = list(a.alphabet[:])

        a.exchange_test(self.grantFromComboBox.currentIndex(), self.grantToComboBox.currentIndex())
        a.check_file()
        for row in range(len(a.name)):
            for col in range(len(alph)):
                chkBoxWidget = QWidget()
                self.chkBox = QCheckBox()

                layoutCheckBox = QHBoxLayout(chkBoxWidget)
                layoutCheckBox.addWidget(self.chkBox)
                layoutCheckBox.setAlignment(Qt.AlignLeft)
                layoutCheckBox.setContentsMargins(0, 0, 0, 0)
                if a.list[a.name[row]][col]:
                    self.chkBox.setChecked(1)
                else:
                    self.chkBox.setChecked(0)

                self.table.setCellWidget(row, col, chkBoxWidget)

    # Вывод верифицированного текста
    def print_text(self):
        self.processedTextEdit.setPlainText('')
        a = GenerTable()
        a.check_file()
        if self.userComboBox.currentText():
            self.processedTextEdit.setPlainText(
                a.verificate_text(self.userComboBox.currentText(), self.sourceTextEdit.toPlainText()))



    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow

        MainWindow.setObjectName("Lab3")
        MainWindow.resize(688, 523)

        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.table = QtWidgets.QTableWidget(self.centralWidget)
        self.table.setObjectName("table")

        # Передаю алфавит
        editTable = GenerTable()
        editTable.check_file()
        alph = list(editTable.alphabet[:])

        self.table.setColumnCount(54)
        self.table.setRowCount(len(editTable.name))

        # Передаю алфавит
        editTable = GenerTable()
        editTable.check_file()
        alph = list(editTable.alphabet[:])

        self.table.setHorizontalHeaderLabels(alph)
        self.table.setVerticalHeaderLabels(editTable.name)

        for row in range(len(editTable.name)):
            for col in range(len(alph)):
                chkBoxWidget = QWidget()
                self.chkBox = QCheckBox()

                layoutCheckBox = QHBoxLayout(chkBoxWidget)
                layoutCheckBox.addWidget(self.chkBox)
                layoutCheckBox.setAlignment(Qt.AlignLeft)
                layoutCheckBox.setContentsMargins(0, 0, 0, 0)
                if editTable.list[editTable.name[row]][col]:
                    self.chkBox.setChecked(1)
                else:
                    self.chkBox.setChecked(0)

                self.table.setCellWidget(row, col, chkBoxWidget)

        # Действие по нажатию на checkbox клетку
        self.table.cellClicked.connect(self.activeCheckBox)
        self.table.cellClicked.connect(self.print_text)

        self.horizontalLayout_3.addWidget(self.table)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")

        self.createLineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.createLineEdit.setObjectName("createLineEdit")

        self.gridLayout.addWidget(self.createLineEdit, 0, 0, 1, 1)

        self.createButton = QtWidgets.QPushButton(self.centralWidget)
        self.createButton.setObjectName("createButton")

        # Добавление нового пользователя
        self.createButton.clicked.connect(self.add_user)

        self.gridLayout.addWidget(self.createButton, 0, 1, 1, 1)

        self.removeComboBox = QtWidgets.QComboBox(self.centralWidget)
        self.removeComboBox.setObjectName("removeComboBox")
        self.removeComboBox.insertItems(0, editTable.name)

        self.gridLayout.addWidget(self.removeComboBox, 1, 0, 1, 1)

        self.removeButton = QtWidgets.QPushButton(self.centralWidget)
        self.removeButton.setObjectName("removeButton")

        # Удаление пользователя
        self.removeButton.clicked.connect(self.test)

        self.gridLayout.addWidget(self.removeButton, 1, 1, 1, 1)

        self.verticalLayout.addLayout(self.gridLayout)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.grantFromComboBox = QtWidgets.QComboBox(self.centralWidget)
        self.grantFromComboBox.setObjectName("grantFromComboBox")
        self.grantFromComboBox.insertItems(0, editTable.name)

        self.horizontalLayout_2.addWidget(self.grantFromComboBox)

        self.grantToComboBox = QtWidgets.QComboBox(self.centralWidget)
        self.grantToComboBox.setObjectName("grantToComboBox")
        self.grantToComboBox.insertItems(0, editTable.name)

        self.horizontalLayout_2.addWidget(self.grantToComboBox)

        self.grantButton = QtWidgets.QPushButton(self.centralWidget)
        self.grantButton.setObjectName("grantButton")

        # Обмен правами доступа
        self.grantButton.clicked.connect(self.exchange)

        self.horizontalLayout_2.addWidget(self.grantButton)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.linEditAlph = QLineEdit()
        self.verticalLayout.addWidget(self.linEditAlph)

        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.sourceTextEdit = QtWidgets.QTextEdit(self.centralWidget)
        self.sourceTextEdit.setObjectName("sourceTextEdit")

        # Преобразование текcта
        self.sourceTextEdit.textChanged.connect(self.print_text)

        self.horizontalLayout.addWidget(self.sourceTextEdit)

        self.processedTextEdit = QtWidgets.QTextEdit(self.centralWidget)
        self.processedTextEdit.setObjectName("processedTextEdit")

        self.horizontalLayout.addWidget(self.processedTextEdit)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.userComboBox = QtWidgets.QComboBox(self.centralWidget)
        self.userComboBox.setObjectName("userComboBox")
        self.userComboBox.insertItem(0, '')
        self.userComboBox.insertItems(1, editTable.name)
        # Преобразование текcта
        self.userComboBox.activated.connect(self.print_text)

        self.verticalLayout_2.addWidget(self.userComboBox)
        MainWindow.setCentralWidget(self.centralWidget)

        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 688, 22))
        self.menuBar.setObjectName("menuBar")

        # MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Lab3"))
        self.createButton.setText(_translate("MainWindow", "Добавить"))
        self.removeButton.setText(_translate("MainWindow", "Удалить"))
        self.grantButton.setText(_translate("MainWindow", "Изменить"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
