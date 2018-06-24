from PyQt5 import QtCore, QtGui, QtWidgets
import functools, os, time
from distutils.dir_util import copy_tree
import shutil
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
                             QAction, QFileDialog, QApplication, QWidget, QAbstractItemView)


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.openDirNameDialog()

        self.show()

    def openDirNameDialog(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.dirName = file


# Класс описывающий роли пользователей и их права
class RoleClass(object):
    def __init__(self):
        self.levelRole = ['Top-Secret', 'Secret', 'Non-Secret']
        self.roleArray = ['Admin', 'Programmer']
        self.roleUSer = ['Sasha', 'Masha']
        self.levels_into_role = {}
        self.user_with_role = {}
        self.levels_into_role = dict.fromkeys(self.roleArray)

        for role in self.levels_into_role:
            self.levels_into_role[role] = self.levelRole

        self.user_with_role = dict.fromkeys(self.roleUSer)

        for user in self.user_with_role:
            self.user_with_role[user] = self.roleArray

    # Перевод массива в строку
    def options_to_str(self, *args):
        strParam = ''
        for i in args:
            strParam += str(i) + ', '

        return strParam[:-2]

    # Перевод строки в массив
    def str_to_param(self, strParam):
        return strParam.split(', ')


# Класс описывающий начальные уровни доступа
class levelsTab(object):
    def __init__(self):
        self.arrPerm = ['Top-Secret', 'Secret', 'Non-Secret']


class Ui_MainWindow(object):
    # Выбор пользователя в комбобоксе
    def print_info(self):
        resultTmp = list()
        for role in self.role.user_with_role[self.comboBox.currentText()]:
            resultTmp += self.role.levels_into_role[role]
        self.result = list(set(resultTmp))
        print(self.result)

    # Отлавливаю коорбинаты комбобокса
    def handleCombo(self, row, index):
        print('Current Row: ' + str(row))
        print('Index of Combo: ' + str(index))

    # Перемещение уровня доступа вверх
    def up_level(self):
        index = self.listView_2.currentRow()
        if index:
            tmpStr = self.level.arrPerm[index]
            tmp = self.listView_2.item(index).text()
            self.level.arrPerm[index] = self.level.arrPerm[index - 1]
            self.level.arrPerm[index - 1] = tmpStr

            self.listView_2.item(index).setText(self.listView_2.item(index - 1).text())
            self.listView_2.item(index - 1).setText(tmp)
            curInd = int(index - 1)
            self.listView_2.setCurrentRow(curInd)
            for index in range(self.tableWidget.rowCount()):
                combo = QtWidgets.QComboBox()
                for i in range(len(self.level.arrPerm)):
                    combo.addItem(self.level.arrPerm[i])

                self.tableWidget.setCellWidget(index, 1, combo)
                combo.currentIndexChanged.connect(functools.partial(self.handleCombo, index))

    # Перемещение уроня доступа вниз
    def down_level(self):
        index = self.listView_2.currentRow()
        if index != len(self.level.arrPerm) - 1:
            tmpStr = self.level.arrPerm[index]
            tmp = self.listView_2.item(index).text()
            self.level.arrPerm[index] = self.level.arrPerm[index + 1]
            self.level.arrPerm[index + 1] = tmpStr

            self.listView_2.item(index).setText(self.listView_2.item(index + 1).text())
            self.listView_2.item(index + 1).setText(tmp)
            curInd = int(index + 1)
            self.listView_2.setCurrentRow(curInd)
            for index in range(self.tableWidget.rowCount()):
                combo = QtWidgets.QComboBox()
                for i in range(len(self.level.arrPerm)):
                    combo.addItem(self.level.arrPerm[i])

                self.tableWidget.setCellWidget(index, 1, combo)
                combo.currentIndexChanged.connect(functools.partial(self.handleCombo, index))

    # Добавление нового уровня
    def add_level(self):
        if self.lineEditLevel.text():
            self.level.arrPerm.append(self.lineEditLevel.text())
            self.listView_2.addItem(self.lineEditLevel.text())
            self.lineEditLevel.setText('')
            self.listView_2.setCurrentRow(len(self.level.arrPerm) - 1)

            for index in range(self.tableWidget.rowCount()):
                combo = QtWidgets.QComboBox()
                for i in range(len(self.level.arrPerm)):
                    combo.addItem(self.level.arrPerm[i])

                self.tableWidget.setCellWidget(index, 1, combo)
                combo.currentIndexChanged.connect(functools.partial(self.handleCombo, index))

    # Удаление уровня
    def del_level(self):
        index = self.listView_2.currentRow()
        self.listView_2.takeItem(index)
        self.level.arrPerm.pop()
        for index in range(self.tableWidget.rowCount()):
            combo = QtWidgets.QComboBox()
            for i in range(len(self.level.arrPerm)):
                combo.addItem(self.level.arrPerm[i])

            self.tableWidget.setCellWidget(index, 1, combo)
            combo.currentIndexChanged.connect(functools.partial(self.handleCombo, index))

    # Добавление папки
    def add_folder(self):
        a = App()
        print(a.dirName)

        self.massivTest = []

        # print(self.tableWidget.item(0, 0).text())

        for j in range(self.tableWidget.rowCount() - 1):
            self.massivTest.append(self.tableWidget.item(j, 0).text())
            print(self.tableWidget.item(j, 0).text())

        if a.dirName not in self.massivTest:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            item = QtWidgets.QTableWidgetItem()
            item.setText(a.dirName)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, item)

            for index in range(self.tableWidget.rowCount()):
                combo = QtWidgets.QComboBox()
                for i in range(len(self.level.arrPerm)):
                    combo.addItem(self.level.arrPerm[i])

                self.tableWidget.setCellWidget(index, 1, combo)
                combo.currentIndexChanged.connect(functools.partial(self.handleCombo, index))

    # Удаление папки
    def del_folder(self):
        self.tableWidget.removeRow(self.tableWidget.currentRow())

    # Тотал командер
    def view_folder(self):
        a = App()

        userLevel = {}

        aNew = []
        dirLevel = []

        test = {}
        for i in range(self.tableWidget.rowCount()):
            aNew.append(self.tableWidget.item(i, 0).text())
            dirLevel.append(self.tableWidget.cellWidget(i, 1).currentText())
            userLevel.update(
                {self.tableWidget.cellWidget(i, 1).currentText(): self.tableWidget.cellWidget(i, 1).currentIndex()})
            test[self.tableWidget.item(i, 0).text()] = self.tableWidget.cellWidget(i, 1).currentIndex()

        print(userLevel)
        print(test)

        for i in range(len(self.result)):
            if self.result[i] in userLevel:
                self.result[i] = userLevel[self.result[i]]
            else:
                self.result[i] = self.tableWidget.rowCount() - 1

        intLevel = min(self.result)
        print(intLevel)
        self.lineEdit.setText(os.path.realpath(a.dirName))
        self.lineEdit_3.setText(os.path.realpath(a.dirName))
        self.lineEdit_10.setText(os.path.realpath(a.dirName))
        if len(a.dirName):
            listDir = os.listdir(a.dirName)
            self.tableWidget_3.setRowCount(0)
            self.tableWidget_5.setRowCount(0)
            self.tableWidget_9.setRowCount(0)

            for i in listDir:
                path = str(a.dirName + '/' + i)
                if os.path.isfile(a.dirName + '/' + i):
                    pass
                else:
                    if path in test:
                        if test[path] >= intLevel:
                            print(path)
                            self.tableWidget_9.insertRow(self.tableWidget_9.rowCount())

                            item3 = QtWidgets.QTableWidgetItem()
                            item3.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                            item3.setText(i)
                            self.tableWidget_9.setItem(self.tableWidget_9.rowCount() - 1, 0, item3)

                            itemTime3 = QtWidgets.QTableWidgetItem()
                            itemTime3.setText(str(time.ctime(os.path.getmtime(a.dirName + '/' + i))))
                            self.tableWidget_9.setItem(self.tableWidget_9.rowCount() - 1, 2, itemTime3)
                    else:
                        self.tableWidget_9.insertRow(self.tableWidget_9.rowCount())

                        item3 = QtWidgets.QTableWidgetItem()
                        item3.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                        item3.setText(i)
                        self.tableWidget_9.setItem(self.tableWidget_9.rowCount() - 1, 0, item3)

                        itemTime3 = QtWidgets.QTableWidgetItem()
                        itemTime3.setText(str(time.ctime(os.path.getmtime(a.dirName + '/' + i))))
                        self.tableWidget_9.setItem(self.tableWidget_9.rowCount() - 1, 2, itemTime3)

                self.tableWidget_3.insertRow(self.tableWidget_3.rowCount())
                self.tableWidget_5.insertRow(self.tableWidget_5.rowCount())

                item = QtWidgets.QTableWidgetItem()
                item.setText(i)
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

                item2 = QtWidgets.QTableWidgetItem()
                item2.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                item2.setText(i)

                self.tableWidget_3.setItem(self.tableWidget_3.rowCount() - 1, 0, item)
                self.tableWidget_5.setItem(self.tableWidget_3.rowCount() - 1, 0, item2)

                if os.path.isfile(a.dirName + '/' + i):
                    itemSize = QtWidgets.QTableWidgetItem()
                    itemSize.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    itemSize.setText(str(os.path.getsize(a.dirName + '/' + i) / 1000) + ' K')
                    itemSize2 = QtWidgets.QTableWidgetItem()
                    itemSize2.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    itemSize2.setText(str(os.path.getsize(a.dirName + '/' + i) / 1000) + ' K')
                    self.tableWidget_3.setItem(self.tableWidget_3.rowCount() - 1, 1, itemSize)
                    self.tableWidget_5.setItem(self.tableWidget_3.rowCount() - 1, 1, itemSize2)

                else:
                    itemDir = QtWidgets.QTableWidgetItem()
                    itemDir.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    itemDir.setText('Папка')

                    itemDir2 = QtWidgets.QTableWidgetItem()
                    itemDir2.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    itemDir2.setText('Папка')

                    itemDir3 = QtWidgets.QTableWidgetItem()
                    itemDir3.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    itemDir3.setText('Папка')

                    self.tableWidget_3.setItem(self.tableWidget_3.rowCount() - 1, 1, itemDir)
                    self.tableWidget_5.setItem(self.tableWidget_3.rowCount() - 1, 1, itemDir2)
                    self.tableWidget_9.setItem(self.tableWidget_9.rowCount() - 1, 1, itemDir3)

                itemTime = QtWidgets.QTableWidgetItem()
                itemTime.setText(str(time.ctime(os.path.getmtime(a.dirName + '/' + i))))
                self.tableWidget_3.setItem(self.tableWidget_3.rowCount() - 1, 2, itemTime)

                itemTime2 = QtWidgets.QTableWidgetItem()
                itemTime2.setText(str(time.ctime(os.path.getmtime(a.dirName + '/' + i))))
                self.tableWidget_5.setItem(self.tableWidget_5.rowCount() - 1, 2, itemTime2)

    # Копирование файла
    def copy_file(self):
        a = []
        dirLevel = []

        test = {}
        for i in range(self.tableWidget.rowCount()):
            a.append(self.tableWidget.item(i, 0).text())
            dirLevel.append(self.tableWidget.cellWidget(i, 1).currentText())
            test[self.tableWidget.item(i, 0).text()] = self.tableWidget.cellWidget(i, 1).currentIndex()

        if self.lineEdit.text() in test:
            if self.lineEdit_3.text() in test:
                print(test[self.lineEdit.text()], test[self.lineEdit_3.text()])
                if test[self.lineEdit.text()] <= test[self.lineEdit_3.text()]:
                    print(test[self.lineEdit.text()], test[self.lineEdit_3.text()])
                    if os.path.isfile(
                            self.lineEdit.text() + '/' + self.tableWidget_3.item(self.tableWidget_3.currentRow(),
                                                                                 0).text()):
                        shutil.copy(
                            self.lineEdit.text() + '/' + self.tableWidget_3.item(self.tableWidget_3.currentRow(),
                                                                                 0).text(),
                            self.lineEdit_3.text())
                    else:
                        shutil.copytree(
                            self.lineEdit.text() + '/' + self.tableWidget_3.item(self.tableWidget_3.currentRow(),
                                                                                 0).text(),
                            self.lineEdit_3.text() + '/' + self.tableWidget_3.item(self.tableWidget_3.currentRow(),
                                                                                   0).text())

                    # Обновление списка файлов
                    dirName = self.lineEdit_3.text()

                    # self.lineEdit.setText(os.path.realpath(dirName))
                    self.lineEdit_3.setText(os.path.realpath(dirName))
                    if len(dirName):
                        listDir = os.listdir(dirName)
                        self.tableWidget_5.setRowCount(0)

                        for i in listDir:
                            self.tableWidget_5.insertRow(self.tableWidget_5.rowCount())
                            item = QtWidgets.QTableWidgetItem()
                            item.setText(i)
                            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

                            self.tableWidget_5.setItem(self.tableWidget_5.rowCount() - 1, 0, item)

                            if os.path.isfile(dirName + '/' + i):
                                itemSize = QtWidgets.QTableWidgetItem()
                                itemSize.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                                itemSize.setText(str(os.path.getsize(dirName + '/' + i) / 1000) + ' K')

                                self.tableWidget_5.setItem(self.tableWidget_5.rowCount() - 1, 1, itemSize)

                            else:
                                itemDir = QtWidgets.QTableWidgetItem()
                                itemDir.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                                itemDir.setText('Папка')

                                self.tableWidget_5.setItem(self.tableWidget_5.rowCount() - 1, 1, itemDir)

                            itemTime = QtWidgets.QTableWidgetItem()
                            itemTime.setText(str(time.ctime(os.path.getmtime(dirName + '/' + i))))
                            self.tableWidget_5.setItem(self.tableWidget_5.rowCount() - 1, 2, itemTime)

        else:
            if not self.lineEdit_3.text() in test:
                if os.path.isfile(
                        self.lineEdit.text() + '/' + self.tableWidget_3.item(self.tableWidget_3.currentRow(),
                                                                             0).text()):
                    shutil.copy(
                        self.lineEdit.text() + '/' + self.tableWidget_3.item(self.tableWidget_3.currentRow(),
                                                                             0).text(),
                        self.lineEdit_3.text())
                else:
                    shutil.copytree(
                        self.lineEdit.text() + '/' + self.tableWidget_3.item(self.tableWidget_3.currentRow(),
                                                                             0).text(),
                        self.lineEdit_3.text() + '/' + self.tableWidget_3.item(self.tableWidget_3.currentRow(),
                                                                               0).text())

                # Обновление списка файлов
                dirName = self.lineEdit_3.text()

                # self.lineEdit.setText(os.path.realpath(dirName))
                self.lineEdit_3.setText(os.path.realpath(dirName))
                if len(dirName):
                    listDir = os.listdir(dirName)
                    self.tableWidget_5.setRowCount(0)

                    for i in listDir:
                        self.tableWidget_5.insertRow(self.tableWidget_5.rowCount())
                        item = QtWidgets.QTableWidgetItem()
                        item.setText(i)
                        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

                        self.tableWidget_5.setItem(self.tableWidget_5.rowCount() - 1, 0, item)

                        if os.path.isfile(dirName + '/' + i):
                            itemSize = QtWidgets.QTableWidgetItem()
                            itemSize.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                            itemSize.setText(str(os.path.getsize(dirName + '/' + i) / 1000) + ' K')

                            self.tableWidget_5.setItem(self.tableWidget_5.rowCount() - 1, 1, itemSize)

                        else:
                            itemDir = QtWidgets.QTableWidgetItem()
                            itemDir.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                            itemDir.setText('Папка')

                            self.tableWidget_5.setItem(self.tableWidget_5.rowCount() - 1, 1, itemDir)

                        itemTime = QtWidgets.QTableWidgetItem()
                        itemTime.setText(str(time.ctime(os.path.getmtime(dirName + '/' + i))))
                        self.tableWidget_5.setItem(self.tableWidget_5.rowCount() - 1, 2, itemTime)

    # Перемещение файла
    def move_file(self):
        a = []
        dirLevel = []

        test = {}
        for i in range(self.tableWidget.rowCount()):
            a.append(self.tableWidget.item(i, 0).text())
            dirLevel.append(self.tableWidget.cellWidget(i, 1).currentText())
            test[self.tableWidget.item(i, 0).text()] = self.tableWidget.cellWidget(i, 1).currentIndex()

        if self.lineEdit.text() in test:
            if self.lineEdit_3.text() in test:
                print(test[self.lineEdit.text()], test[self.lineEdit_3.text()])
                if test[self.lineEdit.text()] <= test[self.lineEdit_3.text()]:
                    print(test[self.lineEdit.text()], test[self.lineEdit_3.text()])
                    if os.path.isfile(
                            self.lineEdit.text() + '/' + self.tableWidget_3.item(self.tableWidget_3.currentRow(),
                                                                                 0).text()):
                        shutil.move(
                            self.lineEdit.text() + '/' + self.tableWidget_3.item(self.tableWidget_3.currentRow(),
                                                                                 0).text(),
                            self.lineEdit_3.text())
                    else:
                        shutil.move(
                            self.lineEdit.text() + '/' + self.tableWidget_3.item(self.tableWidget_3.currentRow(),
                                                                                 0).text(),
                            self.lineEdit_3.text() + '/' + self.tableWidget_3.item(self.tableWidget_3.currentRow(),
                                                                                   0).text())

                    # Обновление списка файлов
                    dirNameLeft = self.lineEdit.text()
                    dirNameRight = self.lineEdit_3.text()

                    self.lineEdit.setText(os.path.realpath(dirNameLeft))
                    self.lineEdit_3.setText(os.path.realpath(dirNameRight))

                    if len(dirNameLeft):
                        listDir = os.listdir(dirNameLeft)
                        self.tableWidget_3.setRowCount(0)

                        for i in listDir:
                            self.tableWidget_3.insertRow(self.tableWidget_3.rowCount())

                            item = QtWidgets.QTableWidgetItem()
                            item.setText(i)
                            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

                            self.tableWidget_3.setItem(self.tableWidget_3.rowCount() - 1, 0, item)

                            if os.path.isfile(dirNameLeft + '/' + i):
                                itemSize = QtWidgets.QTableWidgetItem()
                                itemSize.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                                itemSize.setText(str(os.path.getsize(dirNameLeft + '/' + i) / 1000) + ' K')

                                self.tableWidget_3.setItem(self.tableWidget_3.rowCount() - 1, 1, itemSize)

                            else:
                                itemDir = QtWidgets.QTableWidgetItem()
                                itemDir.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                                itemDir.setText('Папка')

                                self.tableWidget_3.setItem(self.tableWidget_3.rowCount() - 1, 1, itemDir)

                            itemTime = QtWidgets.QTableWidgetItem()
                            itemTime.setText(str(time.ctime(os.path.getmtime(dirNameLeft + '/' + i))))
                            self.tableWidget_3.setItem(self.tableWidget_3.rowCount() - 1, 2, itemTime)

                    if len(dirNameRight):
                        listDir = os.listdir(dirNameRight)
                        self.tableWidget_5.setRowCount(0)

                        for i in listDir:
                            self.tableWidget_5.insertRow(self.tableWidget_5.rowCount())

                            item = QtWidgets.QTableWidgetItem()
                            item.setText(i)
                            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

                            self.tableWidget_5.setItem(self.tableWidget_5.rowCount() - 1, 0, item)

                            if os.path.isfile(dirNameRight + '/' + i):
                                itemSize = QtWidgets.QTableWidgetItem()
                                itemSize.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                                itemSize.setText(str(os.path.getsize(dirNameRight + '/' + i) / 1000) + ' K')

                                self.tableWidget_5.setItem(self.tableWidget_5.rowCount() - 1, 1, itemSize)

                            else:
                                itemDir = QtWidgets.QTableWidgetItem()
                                itemDir.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                                itemDir.setText('Папка')

                                self.tableWidget_5.setItem(self.tableWidget_5.rowCount() - 1, 1, itemDir)

                            itemTime = QtWidgets.QTableWidgetItem()
                            itemTime.setText(str(time.ctime(os.path.getmtime(dirNameRight + '/' + i))))
                            self.tableWidget_5.setItem(self.tableWidget_3.rowCount() - 1, 2, itemTime)



        else:
            if not self.lineEdit_3.text() in test:
                if os.path.isfile(
                        self.lineEdit.text() + '/' + self.tableWidget_3.item(self.tableWidget_3.currentRow(),
                                                                             0).text()):
                    shutil.move(
                        self.lineEdit.text() + '/' + self.tableWidget_3.item(self.tableWidget_3.currentRow(),
                                                                             0).text(),
                        self.lineEdit_3.text())
                else:
                    shutil.move(
                        self.lineEdit.text() + '/' + self.tableWidget_3.item(self.tableWidget_3.currentRow(),
                                                                             0).text(),
                        self.lineEdit_3.text() + '/' + self.tableWidget_3.item(self.tableWidget_3.currentRow(),
                                                                               0).text())

                # Обновление списка файлов
                dirNameLeft = self.lineEdit.text()
                dirNameRight = self.lineEdit_3.text()

                self.lineEdit.setText(os.path.realpath(dirNameLeft))
                self.lineEdit_3.setText(os.path.realpath(dirNameRight))

                if len(dirNameLeft):
                    listDir = os.listdir(dirNameLeft)
                    self.tableWidget_3.setRowCount(0)

                    for i in listDir:
                        self.tableWidget_3.insertRow(self.tableWidget_3.rowCount())

                        item = QtWidgets.QTableWidgetItem()
                        item.setText(i)
                        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

                        self.tableWidget_3.setItem(self.tableWidget_3.rowCount() - 1, 0, item)

                        if os.path.isfile(dirNameLeft + '/' + i):
                            itemSize = QtWidgets.QTableWidgetItem()
                            itemSize.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                            itemSize.setText(str(os.path.getsize(dirNameLeft + '/' + i) / 1000) + ' K')

                            self.tableWidget_3.setItem(self.tableWidget_3.rowCount() - 1, 1, itemSize)

                        else:
                            itemDir = QtWidgets.QTableWidgetItem()
                            itemDir.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                            itemDir.setText('Папка')

                            self.tableWidget_3.setItem(self.tableWidget_3.rowCount() - 1, 1, itemDir)

                        itemTime = QtWidgets.QTableWidgetItem()
                        itemTime.setText(str(time.ctime(os.path.getmtime(dirNameLeft + '/' + i))))
                        self.tableWidget_3.setItem(self.tableWidget_3.rowCount() - 1, 2, itemTime)

                if len(dirNameRight):
                    listDir = os.listdir(dirNameRight)
                    self.tableWidget_5.setRowCount(0)

                    for i in listDir:
                        self.tableWidget_5.insertRow(self.tableWidget_5.rowCount())

                        item = QtWidgets.QTableWidgetItem()
                        item.setText(i)
                        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

                        self.tableWidget_5.setItem(self.tableWidget_5.rowCount() - 1, 0, item)

                        if os.path.isfile(dirNameRight + '/' + i):
                            itemSize = QtWidgets.QTableWidgetItem()
                            itemSize.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                            itemSize.setText(str(os.path.getsize(dirNameRight + '/' + i) / 1000) + ' K')

                            self.tableWidget_5.setItem(self.tableWidget_5.rowCount() - 1, 1, itemSize)

                        else:
                            itemDir = QtWidgets.QTableWidgetItem()
                            itemDir.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                            itemDir.setText('Папка')

                            self.tableWidget_5.setItem(self.tableWidget_5.rowCount() - 1, 1, itemDir)

                        itemTime = QtWidgets.QTableWidgetItem()
                        itemTime.setText(str(time.ctime(os.path.getmtime(dirNameRight + '/' + i))))
                        self.tableWidget_5.setItem(self.tableWidget_3.rowCount() - 1, 2, itemTime)

    # Перемещение в левой части
    def move_in_folder_left(self):

        dirName = self.lineEdit.text() + '/' + self.tableWidget_3.item(self.tableWidget_3.currentRow(), 0).text()

        self.lineEdit.setText(os.path.realpath(dirName))
        # self.lineEdit_3.setText(os.path.realpath(dirName))
        if len(dirName):
            listDir = os.listdir(dirName)
            self.tableWidget_3.setRowCount(0)

            for i in listDir:
                self.tableWidget_3.insertRow(self.tableWidget_3.rowCount())
                item = QtWidgets.QTableWidgetItem()
                item.setText(i)
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

                self.tableWidget_3.setItem(self.tableWidget_3.rowCount() - 1, 0, item)

                if os.path.isfile(dirName + '/' + i):
                    itemSize = QtWidgets.QTableWidgetItem()
                    itemSize.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    itemSize.setText(str(os.path.getsize(dirName + '/' + i) / 1000) + ' K')

                    self.tableWidget_3.setItem(self.tableWidget_3.rowCount() - 1, 1, itemSize)

                else:
                    itemDir = QtWidgets.QTableWidgetItem()
                    itemDir.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    itemDir.setText('Папка')

                    self.tableWidget_3.setItem(self.tableWidget_3.rowCount() - 1, 1, itemDir)

                itemTime = QtWidgets.QTableWidgetItem()
                itemTime.setText(str(time.ctime(os.path.getmtime(dirName + '/' + i))))
                self.tableWidget_3.setItem(self.tableWidget_3.rowCount() - 1, 2, itemTime)

    # Перемещение в правой части
    def move_in_folder_right(self):
        dirName = self.lineEdit_3.text() + '/' + self.tableWidget_5.item(self.tableWidget_5.currentRow(), 0).text()

        # self.lineEdit.setText(os.path.realpath(dirName))
        self.lineEdit_3.setText(os.path.realpath(dirName))
        if len(dirName):
            listDir = os.listdir(dirName)
            self.tableWidget_5.setRowCount(0)

            for i in listDir:
                self.tableWidget_5.insertRow(self.tableWidget_5.rowCount())
                item = QtWidgets.QTableWidgetItem()
                item.setText(i)
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

                self.tableWidget_5.setItem(self.tableWidget_5.rowCount() - 1, 0, item)

                if os.path.isfile(dirName + '/' + i):
                    itemSize = QtWidgets.QTableWidgetItem()
                    itemSize.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    itemSize.setText(str(os.path.getsize(dirName + '/' + i) / 1000) + ' K')

                    self.tableWidget_5.setItem(self.tableWidget_5.rowCount() - 1, 1, itemSize)

                else:
                    itemDir = QtWidgets.QTableWidgetItem()
                    itemDir.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    itemDir.setText('Папка')

                    self.tableWidget_5.setItem(self.tableWidget_5.rowCount() - 1, 1, itemDir)

                itemTime = QtWidgets.QTableWidgetItem()
                itemTime.setText(str(time.ctime(os.path.getmtime(dirName + '/' + i))))
                self.tableWidget_5.setItem(self.tableWidget_5.rowCount() - 1, 2, itemTime)

    # Добавление уровней роли
    def add_levels_role(self):
        row = self.tableWidgetRole.currentRow()
        param = self.lineEdit_4.text()
        self.tableWidgetRole.setItem(row, 1, QtWidgets.QTableWidgetItem(param))
        name = self.tableWidgetRole.item(row, 0).text()
        inputParam = self.role.str_to_param(param)
        self.role.levels_into_role[name] = inputParam

    # Добавление ролей пользователю
    def add_role_user(self):
        row = self.tableWidgetUser.currentRow()
        param = self.lineEdit_6.text()
        self.tableWidgetUser.setItem(row, 1, QtWidgets.QTableWidgetItem(param))
        user = self.tableWidgetUser.item(row, 0).text()
        inputParam = self.role.str_to_param(param)
        self.role.user_with_role[user] = inputParam

    # Удаление уровней роли
    def del_levels_role(self):
        row = self.tableWidgetRole.currentRow()
        a = self.tableWidgetRole.item(row, 1)
        name = self.tableWidgetRole.item(row, 0).text()
        text_ar = a.text().split(', ')
        if self.lineEdit_5.text():
            text_del_ar = self.lineEdit_5.text().split(', ')
            for i in text_del_ar:
                if i in text_ar:
                    text_ar.remove(i)
                    print(name)
                    self.role.levels_into_role[name].remove(i)
                    print(self.role.levels_into_role)

            self.tableWidgetRole.setItem(row, 1, QtWidgets.QTableWidgetItem(', '.join(text_ar)))
            print(self.role.user_with_role)

    # Удаление ролей пользователя
    def del_role_user(self):
        row = self.tableWidgetUser.currentRow()
        a = self.tableWidgetUser.item(row, 1)
        name = self.tableWidgetUser.item(row, 0).text()
        text_ar = a.text().split(', ')
        if self.lineEdit_7.text():
            text_del_ar = self.lineEdit_7.text().split(', ')
            for i in text_del_ar:
                if i in text_ar:
                    text_ar.remove(i)
                    self.role.user_with_role[name].remove(i)
            self.tableWidgetUser.setItem(row, 1, QtWidgets.QTableWidgetItem(', '.join(text_ar)))
            print(self.role.user_with_role)

    # Добавление роли
    def add_role(self):
        if self.lineEdit_8.text():
            current_row = self.tableWidgetRole.rowCount()
            self.tableWidgetRole.insertRow(current_row)
            self.tableWidgetRole.setItem(current_row, 0, QtWidgets.QTableWidgetItem(self.lineEdit_8.text()))
            if self.lineEdit_8.text() not in self.role.roleArray:
                self.role.levels_into_role.update({self.lineEdit_8.text(): None})

    # Добавление пользователя
    def add_user(self):
        if self.lineEdit_9.text():
            current_row = self.tableWidgetUser.rowCount()
            self.tableWidgetUser.insertRow(current_row)
            self.tableWidgetUser.setItem(current_row, 0, QtWidgets.QTableWidgetItem(self.lineEdit_9.text()))
            self.comboBox.addItem(self.lineEdit_9.text())
            if self.lineEdit_9.text() not in self.role.roleUSer:
                self.role.user_with_role.update({self.lineEdit_9.text(): None})

    # Удаление роли
    def del_role(self):
        row = self.tableWidgetRole.currentRow()
        name = self.tableWidgetRole.item(row, 0).text()

        self.role.roleArray.remove(name)
        self.tableWidgetRole.removeRow(row)

    # Удаление пользователя
    def del_user(self):
        row = self.tableWidgetUser.currentRow()
        name = self.tableWidgetUser.item(row, 0).text()
        self.role.roleUSer.remove(name)
        self.role.user_with_role.pop(name)
        self.tableWidgetUser.removeRow(row)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1066, 756)

        self.role = RoleClass()

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setObjectName("tabWidget")

        # --------------LEVELS---------------------------------------------------------------------------------------
        self.Levels = QtWidgets.QWidget()
        self.Levels.setObjectName("Levels")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.Levels)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setObjectName("verticalLayout")

        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.lineEditLevel = QtWidgets.QLineEdit(self.Levels)
        self.lineEditLevel.setObjectName("lineEditLevel")

        self.gridLayout_2.addWidget(self.lineEditLevel, 1, 0, 1, 1)

        self.delButton = QtWidgets.QPushButton(self.Levels)
        self.delButton.setObjectName("delButton")

        self.gridLayout_2.addWidget(self.delButton, 2, 1, 1, 1)

        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(spacerItem)

        self.upButton = QtWidgets.QPushButton(self.Levels)
        self.upButton.setObjectName("upButton")

        self.verticalLayout_4.addWidget(self.upButton)

        self.downButton = QtWidgets.QPushButton(self.Levels)
        self.downButton.setObjectName("downButton")

        self.verticalLayout_4.addWidget(self.downButton)

        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(spacerItem1)

        self.gridLayout_2.addLayout(self.verticalLayout_4, 0, 1, 1, 1)

        self.addButton = QtWidgets.QPushButton(self.Levels)
        self.addButton.setObjectName("addButton")

        self.gridLayout_2.addWidget(self.addButton, 1, 1, 1, 1)

        # Добавление уровня доступа
        self.addButton.clicked.connect(self.add_level)

        #  Удаление уровня доступа
        self.delButton.clicked.connect(self.del_level)

        self.listView_2 = QtWidgets.QListWidget(self.Levels)
        self.listView_2.setProperty("isWrapping", False)
        self.listView_2.setObjectName("listView_2")

        self.level = levelsTab()

        for i in range(len(self.level.arrPerm)):
            self.listView_2.addItem(self.level.arrPerm[i])

        # Повышение и понижение привелегий
        self.upButton.clicked.connect(self.up_level)
        self.downButton.clicked.connect(self.down_level)

        self.gridLayout_2.addWidget(self.listView_2, 0, 0, 1, 1)

        self.verticalLayout.addLayout(self.gridLayout_2)

        self.tabWidget.addTab(self.Levels, "")
        # --------------LEVELS---------------------------------------------------------------------------------------
        self.Folders = QtWidgets.QWidget()
        self.Folders.setObjectName("Folders")

        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.Folders)
        self.verticalLayout_7.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.tableWidget = QtWidgets.QTableWidget(self.Folders)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setGridStyle(QtCore.Qt.DotLine)
        self.tableWidget.setWordWrap(True)
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(3)

        for index in range(self.tableWidget.rowCount()):
            combo = QtWidgets.QComboBox()
            for i in range(len(self.level.arrPerm)):
                combo.addItem(self.level.arrPerm[i])

            self.tableWidget.setCellWidget(index, 1, combo)
            item = QtWidgets.QTableWidgetItem()
            item.setText(os.path.realpath(self.level.arrPerm[index]))
            self.tableWidget.setItem(index, 0, item)
            combo.currentIndexChanged.connect(functools.partial(self.handleCombo, index))

        self.tableWidget.setColumnWidth(0, 400)
        self.tableWidget.setColumnWidth(1, 150)

        self.tableWidget.setHorizontalHeaderLabels(['Папка', 'Уровень секретности'])

        self.horizontalLayout_3.addWidget(self.tableWidget)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.addFolderButton = QtWidgets.QPushButton(self.Folders)
        self.addFolderButton.setObjectName("addFolderButton")

        # Добавление папки
        self.addFolderButton.clicked.connect(self.add_folder)

        self.verticalLayout_3.addWidget(self.addFolderButton)

        self.delFolderButton = QtWidgets.QPushButton(self.Folders)
        self.delFolderButton.setObjectName("delFolderButton")

        # Удаление папки
        self.delFolderButton.clicked.connect(self.del_folder)

        self.verticalLayout_3.addWidget(self.delFolderButton)

        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(spacerItem2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.verticalLayout_7.addLayout(self.horizontalLayout_3)

        self.tabWidget.addTab(self.Folders, "")
        self.File = QtWidgets.QWidget()
        self.File.setObjectName("File")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.File)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        self.tableWidget_2 = QtWidgets.QTableWidget(self.File)
        self.tableWidget_2.setMinimumSize(QtCore.QSize(0, 31))
        self.tableWidget_2.setMaximumSize(QtCore.QSize(16777215, 31))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(1)
        self.tableWidget_2.setRowCount(1)
        self.tableWidget_2.verticalHeader().setVisible(False)
        self.tableWidget_2.horizontalHeader().setVisible(False)

        self.tableItem = QtWidgets.QTableWidgetItem()
        self.tableItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.tableItem.setText('Macintosh HD')
        self.tableWidget_2.setItem(0, 0, self.tableItem)

        self.horizontalLayout_4.addWidget(self.tableWidget_2)

        self.tableWidget_4 = QtWidgets.QTableWidget(self.File)
        self.tableWidget_4.setMinimumSize(QtCore.QSize(0, 31))
        self.tableWidget_4.setMaximumSize(QtCore.QSize(16777215, 31))
        self.tableWidget_4.setObjectName("tableWidget_4")
        self.tableWidget_4.setColumnCount(1)
        self.tableWidget_4.setRowCount(1)

        self.tableWidget_4.verticalHeader().setVisible(False)
        self.tableWidget_4.horizontalHeader().setVisible(False)
        self.tableItem = QtWidgets.QTableWidgetItem()
        self.tableItem.setText('Macintosh HD')
        self.tableItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.tableWidget_4.setItem(0, 0, self.tableItem)

        self.horizontalLayout_4.addWidget(self.tableWidget_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.File)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setReadOnly(True)
        self.horizontalLayout.addWidget(self.lineEdit)

        self.pushButton = QtWidgets.QPushButton(self.File)
        self.pushButton.setObjectName("pushButton")

        # Выбор папки для отображения
        self.pushButton.clicked.connect(self.view_folder)

        self.horizontalLayout.addWidget(self.pushButton)
        self.horizontalLayout_5.addLayout(self.horizontalLayout)

        self.lineEdit_3 = QtWidgets.QLineEdit(self.File)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setReadOnly(True)

        self.horizontalLayout_5.addWidget(self.lineEdit_3)

        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")

        self.label_3 = QtWidgets.QLabel(self.File)
        self.label_3.setObjectName("label_3")

        self.horizontalLayout_6.addWidget(self.label_3)

        self.label_4 = QtWidgets.QLabel(self.File)
        self.label_4.setObjectName("label_4")

        self.horizontalLayout_6.addWidget(self.label_4)

        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")

        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")

        self.tableWidget_3 = QtWidgets.QTableWidget(self.File)
        self.tableWidget_3.setMinimumSize(QtCore.QSize(0, 465))
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setColumnCount(3)
        self.tableWidget_3.setRowCount(0)
        self.tableWidget_3.setShowGrid(False)

        self.tableWidget_3.setHorizontalHeaderLabels(['Имя', 'Размер', 'Дата'])
        self.tableWidget_3.verticalHeader().setVisible(False)

        self.tableWidget_3.setColumnWidth(0, 172)
        self.tableWidget_3.setColumnWidth(1, 160)
        self.tableWidget_3.setColumnWidth(2, 160)
        self.tableWidget_3.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.tableWidget_3.cellDoubleClicked.connect(self.move_in_folder_left)

        self.verticalLayout_6.addWidget(self.tableWidget_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.copyButton = QtWidgets.QPushButton(self.File)
        self.copyButton.setObjectName("copyButton")

        # Копировать файл
        self.copyButton.clicked.connect(self.copy_file)

        self.horizontalLayout_2.addWidget(self.copyButton)

        self.moveButton = QtWidgets.QPushButton(self.File)
        self.moveButton.setObjectName("moveButton")

        # Переместить файл
        self.moveButton.clicked.connect(self.move_file)

        self.horizontalLayout_2.addWidget(self.moveButton)

        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_7.addLayout(self.verticalLayout_6)

        self.tableWidget_5 = QtWidgets.QTableWidget(self.File)
        self.tableWidget_5.setObjectName("tableWidget_5")
        self.tableWidget_5.setColumnCount(3)
        self.tableWidget_5.setRowCount(0)
        self.tableWidget_5.setShowGrid(False)

        self.tableWidget_5.setHorizontalHeaderLabels(['Имя', 'Размер', 'Дата'])
        self.tableWidget_5.verticalHeader().setVisible(False)

        self.tableWidget_5.setColumnWidth(0, 172)
        self.tableWidget_5.setColumnWidth(1, 160)
        self.tableWidget_5.setColumnWidth(2, 160)
        self.tableWidget_5.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.tableWidget_5.cellDoubleClicked.connect(self.move_in_folder_right)

        self.horizontalLayout_7.addWidget(self.tableWidget_5)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.verticalLayout_8.addLayout(self.verticalLayout_2)
        self.tabWidget.addTab(self.File, "")
        self.verticalLayout_5.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1066, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # New--------------------------------------------------
        self.Role = QtWidgets.QWidget()
        self.Role.setObjectName("Role")

        self.verticalLayout_19 = QtWidgets.QVBoxLayout(self.Role)
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setObjectName("verticalLayout_13")

        self.tableWidgetRole = QtWidgets.QTableWidget(self.Role)
        self.tableWidgetRole.setGridStyle(QtCore.Qt.DotLine)
        self.tableWidgetRole.setRowCount(2)
        self.tableWidgetRole.setColumnCount(2)
        self.tableWidgetRole.setHorizontalHeaderLabels(['Роль', 'Уровни доступа'])

        self.tableWidgetRole.setObjectName("tableWidgetRole")

        self.tableWidgetRole.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidgetRole.horizontalHeader().setDefaultSectionSize(201)
        self.tableWidgetRole.horizontalHeader().setMinimumSectionSize(26)
        self.tableWidgetRole.horizontalHeader().setStretchLastSection(True)

        self.tableWidgetRole.verticalHeader().setCascadingSectionResizes(True)
        self.tableWidgetRole.verticalHeader().setHighlightSections(False)
        self.tableWidgetRole.verticalHeader().setSortIndicatorShown(False)

        for i in range(self.tableWidgetRole.rowCount()):
            self.tableWidgetRole.setItem(i, 0, QtWidgets.QTableWidgetItem(self.role.roleArray[i]))
            self.tableWidgetRole.setItem(i, 1,
                                         QtWidgets.QTableWidgetItem(self.role.options_to_str(*self.role.levelRole)))

        self.verticalLayout_13.addWidget(self.tableWidgetRole)
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")

        self.addLevelsRole = QtWidgets.QPushButton(self.Role)
        self.addLevelsRole.setObjectName("addLevelsRole")

        self.addLevelsRole.clicked.connect(self.add_levels_role)

        self.horizontalLayout_8.addWidget(self.addLevelsRole)

        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(spacerItem4)
        self.verticalLayout_9.addLayout(self.horizontalLayout_8)

        self.lineEdit_4 = QtWidgets.QLineEdit(self.Role)
        self.lineEdit_4.setObjectName("lineEdit_4")

        self.verticalLayout_9.addWidget(self.lineEdit_4)
        self.horizontalLayout_13.addLayout(self.verticalLayout_9)
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")

        self.addRole = QtWidgets.QPushButton(self.Role)
        self.addRole.setObjectName("addRole")

        self.addRole.clicked.connect(self.add_role)

        self.horizontalLayout_12.addWidget(self.addRole)

        self.delRole = QtWidgets.QPushButton(self.Role)
        self.delRole.setObjectName("delRole")

        self.delRole.clicked.connect(self.del_role)

        self.horizontalLayout_12.addWidget(self.delRole)

        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(spacerItem5)
        self.verticalLayout_11.addLayout(self.horizontalLayout_12)

        self.lineEdit_8 = QtWidgets.QLineEdit(self.Role)
        self.lineEdit_8.setObjectName("lineEdit_8")

        self.verticalLayout_11.addWidget(self.lineEdit_8)
        self.horizontalLayout_13.addLayout(self.verticalLayout_11)
        self.verticalLayout_12.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")

        self.delLevels = QtWidgets.QPushButton(self.Role)
        self.delLevels.setObjectName("delLevels")

        self.delLevels.clicked.connect(self.del_levels_role)

        self.horizontalLayout_9.addWidget(self.delLevels)

        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(spacerItem6)
        self.verticalLayout_10.addLayout(self.horizontalLayout_9)

        self.lineEdit_5 = QtWidgets.QLineEdit(self.Role)
        self.lineEdit_5.setObjectName("lineEdit_5")

        self.verticalLayout_10.addWidget(self.lineEdit_5)
        self.horizontalLayout_14.addLayout(self.verticalLayout_10)
        self.verticalLayout_12.addLayout(self.horizontalLayout_14)
        self.verticalLayout_13.addLayout(self.verticalLayout_12)
        self.verticalLayout_19.addLayout(self.verticalLayout_13)

        self.tabWidget.addTab(self.Role, "")

        self.Users = QtWidgets.QWidget()
        self.Users.setObjectName("Users")

        self.verticalLayout_18 = QtWidgets.QVBoxLayout(self.Users)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout()
        self.verticalLayout_17.setObjectName("verticalLayout_17")

        self.tableWidgetUser = QtWidgets.QTableWidget(self.Users)
        self.tableWidgetUser.setMinimumSize(QtCore.QSize(0, 0))
        self.tableWidgetUser.setGridStyle(QtCore.Qt.DotLine)
        self.tableWidgetUser.setRowCount(2)
        self.tableWidgetUser.setColumnCount(2)
        self.tableWidgetUser.setObjectName("tableWidgetUser")

        self.tableWidgetUser.setHorizontalHeaderLabels(['Пользователь', 'Роли'])
        self.tableWidgetUser.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidgetUser.horizontalHeader().setDefaultSectionSize(168)
        self.tableWidgetUser.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetUser.verticalHeader().setCascadingSectionResizes(True)
        self.tableWidgetUser.verticalHeader().setHighlightSections(False)

        for i in range(self.tableWidgetUser.rowCount()):
            self.tableWidgetUser.setItem(i, 0, QtWidgets.QTableWidgetItem(self.role.roleUSer[i]))
            self.tableWidgetUser.setItem(i, 1,
                                         QtWidgets.QTableWidgetItem(self.role.options_to_str(*self.role.roleArray)))
        # print(self.role.userRole)
        self.verticalLayout_17.addWidget(self.tableWidgetUser)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout()
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")

        self.addRoleUser = QtWidgets.QPushButton(self.Users)
        self.addRoleUser.setObjectName("addRoleUser")

        self.addRoleUser.clicked.connect(self.add_role_user)

        self.horizontalLayout_10.addWidget(self.addRoleUser)

        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(spacerItem7)
        self.verticalLayout_15.addLayout(self.horizontalLayout_10)

        self.lineEdit_6 = QtWidgets.QLineEdit(self.Users)
        self.lineEdit_6.setObjectName("lineEdit_6")

        self.verticalLayout_15.addWidget(self.lineEdit_6)
        self.horizontalLayout_16.addLayout(self.verticalLayout_15)
        self.verticalLayout_16 = QtWidgets.QVBoxLayout()
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")

        self.addUser = QtWidgets.QPushButton(self.Users)
        self.addUser.setObjectName("addUser")

        self.addUser.clicked.connect(self.add_user)

        self.horizontalLayout_15.addWidget(self.addUser)

        self.delUser = QtWidgets.QPushButton(self.Users)
        self.delUser.setObjectName("delUser")

        self.delUser.clicked.connect(self.del_user)

        self.horizontalLayout_15.addWidget(self.delUser)

        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.horizontalLayout_15.addItem(spacerItem8)
        self.verticalLayout_16.addLayout(self.horizontalLayout_15)

        self.lineEdit_9 = QtWidgets.QLineEdit(self.Users)
        self.lineEdit_9.setObjectName("lineEdit_9")

        self.verticalLayout_16.addWidget(self.lineEdit_9)
        self.horizontalLayout_16.addLayout(self.verticalLayout_16)
        self.verticalLayout_17.addLayout(self.horizontalLayout_16)
        self.verticalLayout_14 = QtWidgets.QVBoxLayout()
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")

        self.delRoleUser = QtWidgets.QPushButton(self.Users)
        self.delRoleUser.setObjectName("delRoleUser")

        self.delRoleUser.clicked.connect(self.del_role_user)

        self.horizontalLayout_11.addWidget(self.delRoleUser)

        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(spacerItem9)
        self.verticalLayout_14.addLayout(self.horizontalLayout_11)

        self.lineEdit_7 = QtWidgets.QLineEdit(self.Users)
        self.lineEdit_7.setObjectName("lineEdit_7")

        self.verticalLayout_14.addWidget(self.lineEdit_7)
        self.verticalLayout_17.addLayout(self.verticalLayout_14)
        self.verticalLayout_18.addLayout(self.verticalLayout_17)

        self.tabWidget.addTab(self.Users, "")

        self.UserMode = QtWidgets.QWidget()
        self.UserMode.setObjectName("UserMode")
        self.verticalLayout_20 = QtWidgets.QVBoxLayout(self.UserMode)
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.tableWidget_8 = QtWidgets.QTableWidget(self.UserMode)
        self.tableWidget_8.setMinimumSize(QtCore.QSize(0, 31))
        self.tableWidget_8.setMaximumSize(QtCore.QSize(16777215, 31))
        self.tableWidget_8.setObjectName("tableWidget_8")
        self.tableWidget_8.setColumnCount(1)
        self.tableWidget_8.setRowCount(1)
        self.tableWidget_8.verticalHeader().setVisible(False)
        self.tableWidget_8.horizontalHeader().setVisible(False)
        self.tableItemTwo = QtWidgets.QTableWidgetItem()
        self.tableItemTwo.setText('Macintosh HD')
        self.tableItemTwo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.tableWidget_8.setItem(0, 0, self.tableItemTwo)
        self.verticalLayout_20.addWidget(self.tableWidget_8)
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.label = QtWidgets.QLabel(self.UserMode)
        self.label.setObjectName("label")
        self.horizontalLayout_18.addWidget(self.label)

        self.comboBox = QtWidgets.QComboBox(self.UserMode)
        self.comboBox.setObjectName("comboBox")

        for index in range(self.tableWidgetUser.rowCount()):
            self.comboBox.addItem(self.tableWidgetUser.item(index, 0).text())

        self.comboBox.activated.connect(self.print_info)

        self.horizontalLayout_18.addWidget(self.comboBox)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_18.addItem(spacerItem10)
        self.verticalLayout_20.addLayout(self.horizontalLayout_18)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.lineEdit_10 = QtWidgets.QLineEdit(self.UserMode)
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.horizontalLayout_17.addWidget(self.lineEdit_10)
        self.folderUser = QtWidgets.QPushButton(self.UserMode)
        self.folderUser.setObjectName("folderUser")
        # доделать
        self.folderUser.clicked.connect(self.view_folder)

        self.horizontalLayout_17.addWidget(self.folderUser)
        self.verticalLayout_20.addLayout(self.horizontalLayout_17)
        self.tableWidget_9 = QtWidgets.QTableWidget(self.UserMode)
        self.tableWidget_9.setMinimumSize(QtCore.QSize(0, 465))
        self.tableWidget_9.setObjectName("tableWidget_9")
        self.tableWidget_9.setColumnCount(3)
        self.tableWidget_9.setRowCount(0)
        self.tableWidget_9.setHorizontalHeaderLabels(['Имя', 'Размер', 'Дата'])
        self.tableWidget_9.verticalHeader().setVisible(False)
        self.tableWidget_9.setColumnWidth(0, 172)
        self.tableWidget_9.setColumnWidth(1, 160)
        self.tableWidget_9.setColumnWidth(2, 160)
        self.tableWidget_9.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout_20.addWidget(self.tableWidget_9)

        self.tabWidget.addTab(self.UserMode, "")

        self.verticalLayout_5.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 815, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # --------------------------------------------------------

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.delButton.setText(_translate("MainWindow", "Удалить"))
        self.upButton.setText(_translate("MainWindow", "Наверх"))
        self.downButton.setText(_translate("MainWindow", "Вниз"))
        self.addButton.setText(_translate("MainWindow", "Добавить"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Levels), _translate("MainWindow", "Уровни"))
        self.tableWidget.setSortingEnabled(False)

        self.addFolderButton.setText(_translate("MainWindow", "Добавить папку"))
        self.delFolderButton.setText(_translate("MainWindow", "Удалить папку"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Folders), _translate("MainWindow", "Папка"))
        self.pushButton.setText(_translate("MainWindow", "R"))
        self.label_3.setText(_translate("MainWindow", "Уровень конфедициальности:"))
        self.label_4.setText(_translate("MainWindow", "Уровень конфедициальности:"))
        self.copyButton.setText(_translate("MainWindow", "Копировать"))
        self.moveButton.setText(_translate("MainWindow", "Переместить"))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.File), _translate("MainWindow", "Работа с файлами"))
        self.addLevelsRole.setText(_translate("MainWindow", "Добавить уровни"))
        self.addRole.setText(_translate("MainWindow", "Добавить роль"))
        self.delRole.setText(_translate("MainWindow", "Удалить роль"))
        self.delLevels.setText(_translate("MainWindow", "Удалить уровни"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Role), _translate("MainWindow", "Роль"))
        self.addRoleUser.setText(_translate("MainWindow", "Добавить роли"))
        self.addUser.setText(_translate("MainWindow", "Добавить пользователя"))
        self.delUser.setText(_translate("MainWindow", "Удалить пользователя"))
        self.delRoleUser.setText(_translate("MainWindow", "Удалить роли"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Users), _translate("MainWindow", "Пользователь"))
        self.label.setText(_translate("MainWindow", "Выбор пользователя:"))
        self.folderUser.setText(_translate("MainWindow", "R"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.UserMode), _translate("MainWindow", "Режим пользователя"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
