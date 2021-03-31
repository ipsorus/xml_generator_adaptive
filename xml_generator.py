# Владелец интеллектуальной собственности и разработчик данного программного обеспечения: Лошкарев Вадим Игоревич
# Программное обеспечение: Генератор файлов в формате XML для партий СИ
# e-mail:ipsorus@inbox.ru

#Указатель версии ПО (для заставки и раздела Информация)
version = "Версия программы: 2.2"

import sys
import os
import errno

import instruction  #модуль инструкции
import start_logo  #модуль заставки
import xml_generator_front  #модуль главного окна PyQt

from datetime import datetime, date, time
import time as timer
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QDate, QDateTime, QTimer, QRect
from PyQt5.QtWidgets import QApplication, QCalendarWidget, QFileDialog, QLineEdit, QLabel, QMainWindow, QMenu, QMessageBox, QPushButton, QProgressBar, QSpinBox, QStyleFactory, QTabBar, QTextEdit, QToolButton, QVBoxLayout, QWidget, QWidgetAction

from PyQt5.QtGui import QFont

class Instruction(QtWidgets.QWidget, instruction.Ui_Form):
    def __init__(self, parent=None):
        super(Instruction, self).__init__(parent)
        self.setupUi(self)

class Logo(QtWidgets.QWidget, start_logo.Ui_Form):
    def __init__(self, parent=None):
        super(Logo, self).__init__(parent)

        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        #Указатель версии ПО (для заставки и раздела Информация)
        self.label_2.setText(version)

        self.show()
        self.value = 0
        while self.value <= 400000:
            self.value += 1
            QtWidgets.QApplication.processEvents()
        self.close()

class Menu(QMenu):
    '''
    Наследование от класса QMenu, переназначена функция показа меню для полей Дата поверки и Действительна до
    '''
    def showEvent(self, event):
        if self.isVisible():
            button = self.parentWidget()
            if button is not None:
                pos = button.mapToGlobal(button.rect().bottomLeft())
                self.move(pos - self.rect().topLeft())
        super().showEvent(event)

class Calendar(QtWidgets.QMainWindow):
    def __init__(self, lineEdit, parent=None):
        super().__init__(parent)
        self.toolbutton = QToolButton(popupMode=QToolButton.InstantPopup)
        self.widget = QCalendarWidget()
        self.widget.setEnabled(True)
        self.widget.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.widget.setMinimumSize(QtCore.QSize(0, 165))
        self.widget.setMaximumSize(QtCore.QSize(16777215, 165))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.widget.setFont(font)
        self.widget.setAutoFillBackground(False)
        self.widget.setMinimumDate(QtCore.QDate(0000, 1, 1))
        self.widget.setMaximumDate(QtCore.QDate(9999, 12, 31))
        self.widget.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.widget.setNavigationBarVisible(True)
        self.widget.setDateEditEnabled(True)
        self.widget.setSelectedDate(QDate.currentDate())
        self.widget.setObjectName("calendarWidget")

        self.widget_form = QWidget()
        self.widgetLayout = QVBoxLayout(self.widget_form)
        self.widgetPushButton = QPushButton()
        self.widgetPushButton.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.widgetPushButton.setText("Очистить")
        self.widgetPushButton.setFlat(True)
        self.widgetLayout.addWidget(self.widget)
        self.widgetLayout.addWidget(self.widgetPushButton)

        self.widgetAction = QWidgetAction(lineEdit)
        self.widgetAction.setDefaultWidget(self.widget_form)

        self.widgetMenu = Menu(lineEdit)
        self.widgetMenu.addAction(self.widgetAction)
        self.toolbutton.setMenu(self.widgetMenu)
        #self.widgetPushButton.clicked.connect(lineEdit.clear)

    def setSelectedDate(self, date):
        self.widget.setSelectedDate(date)

class TabPage_SO(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.gridLayout_8 = QtWidgets.QGridLayout(self)
        self.gridLayout_8.setObjectName("self.gridLayout_8")
        self.labelSpecifications = QtWidgets.QLabel("Метрологические характеристики СО", self)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.labelSpecifications.setFont(font)
        self.labelSpecifications.setObjectName("self.labelSpecifications")
        self.gridLayout_8.addWidget(self.labelSpecifications, 2, 0, 1, 1)
        self.labelSerialNumber = QtWidgets.QLabel("Заводской №/№ партии", self)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.labelSerialNumber.setFont(font)
        self.labelSerialNumber.setObjectName("self.labelSerialNumber")
        self.gridLayout_8.addWidget(self.labelSerialNumber, 0, 2, 1, 1)
        self.labelType = QtWidgets.QLabel("№ типа СО по реестру *", self)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.labelType.setFont(font)
        self.labelType.setObjectName("self.labelType")
        self.gridLayout_8.addWidget(self.labelType, 0, 0, 1, 1)
        self.labelYearOfIssue = QtWidgets.QLabel("Год выпуска *", self)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.labelYearOfIssue.setFont(font)
        self.labelYearOfIssue.setObjectName("self.labelYearOfIssue")
        self.gridLayout_8.addWidget(self.labelYearOfIssue, 0, 1, 1, 1)
        self.lineEditSerialNumber = QtWidgets.QLineEdit(self)
        self.lineEditSerialNumber.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lineEditSerialNumber.setFont(font)
        self.lineEditSerialNumber.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.lineEditSerialNumber.setClearButtonEnabled(False)
        self.lineEditSerialNumber.setObjectName("self.lineEditSerialNumber")
        self.gridLayout_8.addWidget(self.lineEditSerialNumber, 1, 2, 1, 1)
        self.lineEditSpecifications = QtWidgets.QLineEdit(self)
        self.lineEditSpecifications.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lineEditSpecifications.setFont(font)
        self.lineEditSpecifications.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.lineEditSpecifications.setClearButtonEnabled(False)
        self.lineEditSpecifications.setObjectName("self.lineEditSpecifications")
        self.gridLayout_8.addWidget(self.lineEditSpecifications, 3, 0, 1, 3)
        self.lineEditType = QtWidgets.QLineEdit(self)
        self.lineEditType.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lineEditType.setFont(font)
        self.lineEditType.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.lineEditType.setClearButtonEnabled(False)
        self.lineEditType.setObjectName("self.lineEditType")
        self.gridLayout_8.addWidget(self.lineEditType, 1, 0, 1, 1)
        self.spinBoxManufYear = QtWidgets.QSpinBox(self)
        self.spinBoxManufYear.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.spinBoxManufYear.setFont(font)
        self.spinBoxManufYear.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.spinBoxManufYear.setMinimum(1917)
        self.spinBoxManufYear.setMaximum(2060)
        current_date = date.today()
        self.spinBoxManufYear.setProperty("value", current_date.year)
        self.spinBoxManufYear.setObjectName("self.spinBoxManufYear")
        self.gridLayout_8.addWidget(self.spinBoxManufYear, 1, 1, 1, 1)

class TabPage_SI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.gridLayout_19 = QtWidgets.QGridLayout(self)
        self.gridLayout_19.setObjectName("self.gridLayout_19")
        self.labelTypeSI = QtWidgets.QLabel("Регистрационный № типа СИ *", self)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.labelTypeSI.setFont(font)
        self.labelTypeSI.setObjectName("self.labelTypeSI")
        self.gridLayout_19.addWidget(self.labelTypeSI, 0, 0, 1, 1)
        self.labelZavNumber = QtWidgets.QLabel("Заводской номер *", self)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.labelZavNumber.setFont(font)
        self.labelZavNumber.setObjectName("self.labelZavNumber")
        self.gridLayout_19.addWidget(self.labelZavNumber, 2, 0, 1, 1)
        self.labelInventory = QtWidgets.QLabel("Буквенно-цифровое обозначение *", self)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.labelInventory.setFont(font)
        self.labelInventory.setObjectName("self.labelInventory")
        self.gridLayout_19.addWidget(self.labelInventory, 2, 1, 1, 1)
        self.lineEditZavNumber = QtWidgets.QLineEdit(self)
        self.lineEditZavNumber.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lineEditZavNumber.setFont(font)
        self.lineEditZavNumber.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.lineEditZavNumber.setClearButtonEnabled(False)
        self.lineEditZavNumber.setObjectName("self.lineEditZavNumber")
        self.gridLayout_19.addWidget(self.lineEditZavNumber, 3, 0, 1, 1)
        self.lineEditInventory = QtWidgets.QLineEdit(self)
        self.lineEditInventory.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lineEditInventory.setFont(font)
        self.lineEditInventory.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.lineEditInventory.setClearButtonEnabled(False)
        self.lineEditInventory.setObjectName("self.lineEditInventory")
        self.gridLayout_19.addWidget(self.lineEditInventory, 3, 1, 1, 1)
        self.lineEditTypeSI = QtWidgets.QLineEdit(self)
        self.lineEditTypeSI.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lineEditTypeSI.setFont(font)
        self.lineEditTypeSI.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.lineEditTypeSI.setClearButtonEnabled(False)
        self.lineEditTypeSI.setObjectName("self.lineEditTypeSI")
        self.gridLayout_19.addWidget(self.lineEditTypeSI, 1, 0, 1, 2)

class main_window(QtWidgets.QMainWindow, xml_generator_front.Ui_MainWindow):
    resized = QtCore.pyqtSignal()                                            #Сигнал на изменение размера основного окна программы

    def __init__(self, parent = None):
        super(main_window, self).__init__()
        self.setupUi(self)

        self.resized.connect(self.resizeInstruction)

        self.instruction = Instruction(self)                                 #Экземпляр инструкции
        self.instruction.hide()
        self.instruction.pushButton.clicked.connect(self.close_instruction)

        self.calendar_vrf = Calendar(self.lineEdit_9)                        #Экземпляры календарей для даты поверки
        self.calendar_vrf.widget.clicked.connect(self.vrf_date)
        self.calendar_valid = Calendar(self.lineEdit_10)
        self.calendar_valid.widget.clicked.connect(self.valid_date)

        self.tabWidget_2.removeTab(0)
        self.tabWidget_3.removeTab(0)

        self.vrfDate = self.lineEdit_9.text()                               #запись исходных значений полей Дата поверки и Действительна до
        self.validDate = self.lineEdit_10.text()

        self.lineEdit_9.installEventFilter(self)                            #установка действия Event (фокус на поле, крусор на поле, курсор убран), для открывания календарей
        self.lineEdit_10.installEventFilter(self)

        self.line.setVisible(False)
        self.line_2.setVisible(False)
        self.line_3.setVisible(False)
        self.line_4.setVisible(False)
        self.label_43.hide()                                                 #сообщение об ошибке в поле Дата поверки и Действительна до
        self.label_24.hide()                                                 #сообщение об ошибке в средствах поверки
        self.pushButton.setEnabled(False)

        self.pushButton.clicked.connect(self.create)                         #Запуск
        self.action.triggered.connect(self.instruction_page_open)
        self.action_2.triggered.connect(self.info_page)
        self.action_4.triggered.connect(self.close)

        self.radioButton_8.toggled.connect(self.onClicked_applic_inapplic)
        self.radioButton.toggled.connect(self.onClicked_type_SI)
        self.radioButton_2.toggled.connect(self.onClicked_type_SI)
        self.radioButton_3.toggled.connect(self.onClicked_type_SI)

        self.radioButton_4.toggled.connect(self.onClicked_zavNumber)
        self.radioButton_5.toggled.connect(self.onClicked_zavNumber)

        self.checkBox_4.toggled.connect(self.onClicked_checkBox_4)

        self.comboBox.activated.connect(self.onClicked_comboBox)
        self.tabWidget.currentChanged.connect(self.test_filled_tabs)
        self.toolBox.currentChanged.connect(self.create_first_tabs)

        self.tabWidget_2.tabCloseRequested.connect(self.closeTab_SO)
        self.tabWidget_3.tabCloseRequested.connect(self.closeTab_SI)

        self.calendar_vrf.widgetPushButton.clicked.connect(self.vrfDateClear)
        self.calendar_valid.widgetPushButton.clicked.connect(self.validDateClear)

        self.tabCurrIndex = self.tabWidget.currentIndex()                    #запись исходного индекса вкладки (для проверки заполнения таб-ов)

        #Проверка на-лету вкладка 1
        self.lineEdit.textChanged.connect(self.check_tab_1)
        self.lineEdit_2.textChanged.connect(self.check_tab_1)
        self.lineEdit_3.textChanged.connect(self.check_tab_1)
        self.lineEdit_4.textChanged.connect(self.check_tab_1)
        self.lineEdit_27.textChanged.connect(self.check_tab_1)
        self.lineEdit_29.textChanged.connect(self.check_tab_1)
        self.spinBox.valueChanged.connect(self.check_tab_1)
        #Проверка на-лету вкладка 2
        self.lineEdit_7.textChanged.connect(self.check_tab_2)
        self.lineEdit_8.textChanged.connect(self.check_tab_2)
        self.lineEdit_9.editingFinished.connect(self.dateValidator)
        self.lineEdit_10.editingFinished.connect(self.dateValidator)
        self.lineEdit_11.textChanged.connect(self.check_tab_2)
        self.lineEdit_13.textChanged.connect(self.check_tab_2)
        #Проверка на-лету вкладка 3
        self.lineEdit_15.textChanged.connect(self.check_tab_3)
        self.lineEdit_16.textChanged.connect(self.check_tab_3)
        self.lineEdit_17.textChanged.connect(self.check_tab_3)
        self.lineEdit_18.textChanged.connect(self.check_tab_3)
        self.comboBox.currentIndexChanged.connect(self.check_tab_3)
        #Проверка на-лету вкладка 4
        self.lineEdit_19.textChanged.connect(self.check_tab_4)
        self.lineEdit_20.textChanged.connect(self.check_tab_4)
        self.lineEdit_21.textChanged.connect(self.check_tab_4)
        self.textEdit_3.textChanged.connect(self.check_tab_4)

        self.indicator_1 = False                                             #индикаторы для вызова разных типов проверок заполнения вкладок
        self.indicator_2 = False                                             #(проверка только текущего поля (False), проверка всех полей вкладки (True))
        self.indicator_3 = False
        self.indicator_4 = False

        self.count_1 = 0                                                     #счетчик заполнения вкладок, если все счетчики установятся в 1, то можно генерировать xml
        self.count_2 = 0
        self.count_3 = 0
        self.count_4 = 0

#==========================

    def vrfDateClear(self):
        self.vrfDate = ''
        self.lineEdit_9.setText('')
        self.lineEdit_9.setStyleSheet(style_line)

    def validDateClear(self):
        self.check_tab_2
        self.validDate = ''
        self.lineEdit_10.setText('')

    def eventFilter(self, obj, event):
        '''
        Действия Event для полей self.lineEdit_9 и self.lineEdit_10. Для работы с календарями.
        '''
        if event.type() == QtCore.QEvent.FocusIn:
            if obj == self.lineEdit_9:
                self.calendar_vrf.toolbutton.showMenu()
            elif obj == self.lineEdit_10:
                self.calendar_valid.toolbutton.showMenu()
        elif event.type() == QtCore.QEvent.Enter:
            if obj == self.lineEdit_9:
                self.lineEdit_9.setReadOnly(False)
            elif obj == self.lineEdit_10:
                self.lineEdit_10.setReadOnly(False)
        elif event.type() == QtCore.QEvent.Leave:
            if obj == self.lineEdit_9:
                self.lineEdit_9.setReadOnly(True)
            elif obj == self.lineEdit_10:
                self.lineEdit_10.setReadOnly(True)
        return super().eventFilter(obj, event)
    #=============================
    #Установка даты в формате "dd.MM.yyyy" в поле Дата поверки
    def vrf_date(self):
        self.calendar_vrf.widgetMenu.close()
        self.lineEdit_9.setText(self.calendar_vrf.widget.selectedDate().toString("dd.MM.yyyy"))
        self.vrfDate = self.calendar_vrf.widget.selectedDate().toString("yyyy-MM-dd")
        self.lineEdit_9.clearFocus()
        self.lineEdit_9.setReadOnly(True)
    #=============================
    #Установка даты в формате "dd.MM.yyyy" в поле Действительна до
    def valid_date(self):
        self.calendar_valid.widgetMenu.close()
        self.lineEdit_10.setText(self.calendar_valid.widget.selectedDate().toString("dd.MM.yyyy"))
        self.validDate = self.calendar_valid.widget.selectedDate().toString("yyyy-MM-dd")
        self.lineEdit_10.clearFocus()
        self.lineEdit_10.setReadOnly(True)
    #=============================
    def dateValidator(self):
        '''
        Валидатор даты, введенной пользователем вручную (без календаря), а также установка пользовательской даты в календарь
        '''
        sender = self.sender()
        if sender.text() == '':
            sender.setText('')
            if sender == self.lineEdit_9:
                self.vrfDate = sender.text()
                self.check_tab_2()
            elif sender == self.lineEdit_10:
                self.validDate = sender.text()
                self.check_tab_2()
        else:
            try:
                self.formattedDate = datetime.strptime(sender.text(),'%d.%m.%Y').strftime('%Y-%m-%d')
                if sender == self.lineEdit_9:
                    self.vrfDate = self.formattedDate
                    sender.setText(datetime.strptime(sender.text(),'%d.%m.%Y').strftime('%d.%m.%Y'))
                    self.split_vrfdate = self.formattedDate.split('-')
                    date = QDate(int(self.split_vrfdate[0]), int(self.split_vrfdate[1]), int(self.split_vrfdate[2]))
                    self.calendar_vrf.setSelectedDate(date)
                    self.check_tab_2()
                elif sender == self.lineEdit_10:
                    self.validDate = self.formattedDate
                    sender.setText(datetime.strptime(sender.text(),'%d.%m.%Y').strftime('%d.%m.%Y'))
                    self.split_validdate = self.formattedDate.split('-')
                    date = QDate(int(self.split_validdate[0]), int(self.split_validdate[1]), int(self.split_validdate[2]))
                    self.calendar_valid.setSelectedDate(date)
                    self.check_tab_2()
            except ValueError:
                if sender == self.lineEdit_9:
                    sender.setText(datetime.strptime(self.vrfDate,'%Y-%m-%d').strftime('%d.%m.%Y'))
                elif sender == self.lineEdit_10:
                    sender.setText(datetime.strptime(self.validDate,'%Y-%m-%d').strftime('%d.%m.%Y'))
                self.check_tab_2()
        
    #=============================
    #Служебные функции
    def instruction_page_open(self):
        self.menubar.setVisible(False)
        self.instruction.show()

    def close_instruction(self):
        self.menubar.setVisible(True)
        self.instruction.close()

    def resizeEvent(self, event):
        self.resized.emit()
        return super(main_window, self).resizeEvent(event)

    def resizeInstruction(self):
        '''
        Получение размеров основного окна и изменение размера окна инструкции. Динамически изменяется размер окна инструкции.
        '''
        self.mainHeight = self.height()
        self.mainWidth = self.width()
        self.instruction.resize(self.mainWidth, self.mainHeight)

    def info_page(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Информация")
        msg.setText("Программное обеспечение: Генератор файлов в формате XML для партий СИ")
        msg.setInformativeText(f"Разработчик: ФГУП \"ВНИИМС\"\nРаспространяется на безвозмездной основе\n{version}\n\nТехническая поддержка: fgis2@gost.ru")
        #msg.setDetailedText(f"Распространяется на безвозмездной основеВерсия программы: 2.0")
        okButton = msg.addButton('Закрыть', QtWidgets.QMessageBox.AcceptRole)
        msg.exec()

    def hidePushButtonShowProgressBar(self):
        '''
        Скрытие кнопки Создать файл (self.pushButton) и создание self.progressBar на месте кнопки
        '''
        self.pushButton.hide()
        self.progressBar = QtWidgets.QProgressBar(self.widget_header)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setMaximumSize(QtCore.QSize(16777215, 30))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_2.addWidget(self.progressBar, 1, 2, 1, 1)

    def statusTimer(self):
        self.timer = QtCore.QTimer()
        self.timer.start(2500)
        self.timer.timeout.connect(self.clearStatusBar)
        self.timer.timeout.connect(self.showButtonStatus)
        self.timer.setSingleShot(True)                                       #Таймер выполняется один раз

    def clearStatusBar(self):
        self.statusBar().clearMessage()

    def showButtonStatus(self):
        self.tabWidget.setEnabled(True)
        self.pushButton.setEnabled(True)
        self.pushButton.setText("Создать xml-файл")

    def closeEvent(self, event):                                             #Запрос на закрытие программы
        reply = QtWidgets.QMessageBox.question(self, 'Предупреждение',
            "Закрыть приложение?", QtWidgets.QMessageBox.No |
            QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, e):                                              #Выход из программы по Esc
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
        if e.key() in [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]:
            self.start_to_create_application()
    #=========================
    #Создание и удаление табов (вкладок)
    def create_first_tabs(self):
        if self.toolBox.currentIndex() == 2 and self.tabWidget_2.count() == 0:
            self.comboBox.setEnabled(False)
            count = self.tabWidget_2.count()
            self.nb_SO = QtWidgets.QToolButton(text="Добавить СО", autoRaise=True)
            self.nb_SO.clicked.connect(self.add_tab_SO)
            self.tabWidget_2.insertTab(count, QtWidgets.QWidget(), "")
            self.tabWidget_2.tabBar().setTabButton(count, QtWidgets.QTabBar.RightSide, self.nb_SO)
            self.toolBox.setItemText(2, '> Стандартные образцы, применяемые при поверке')
            self.add_tab_SO()

        elif self.toolBox.currentIndex() == 4 and self.tabWidget_3.count() == 0:
            self.comboBox.setEnabled(False)
            count_SI = self.tabWidget_3.count()
            self.nb_SI = QtWidgets.QToolButton(text="Добавить СИ", autoRaise=True)
            self.nb_SI.clicked.connect(self.add_tab_SI)
            self.tabWidget_3.insertTab(count_SI, QtWidgets.QWidget(), "")
            self.tabWidget_3.tabBar().setTabButton(count_SI, QtWidgets.QTabBar.RightSide, self.nb_SI)
            self.toolBox.setItemText(4, '> СИ, применяемые при поверке')
            self.add_tab_SI()

    def add_tab_SO(self):
        self.nb_SO.setEnabled(False)
        self.count_3 = 0
        self.start_to_create_application()
        text = f'Образец'
        index = self.tabWidget_2.count() - 1
        tabPage_SO = TabPage_SO(self)
        self.tabWidget_2.insertTab(index, tabPage_SO, text)
        self.tabWidget_2.setCurrentIndex(self.tabWidget_2.count() - 2)
        self.tabWidget_2.currentWidget().lineEditType.textChanged.connect(self.check_tab_3)

    def add_tab_SI(self):
        self.nb_SI.setEnabled(False)
        self.count_3 = 0
        self.start_to_create_application()
        text = f'СИ'
        index = self.tabWidget_3.count() - 1
        tabPage_SI = TabPage_SI(self)
        self.tabWidget_3.insertTab(index, tabPage_SI, text)
        self.tabWidget_3.setCurrentIndex(self.tabWidget_3.count() - 2)
        self.tabWidget_3.currentWidget().lineEditTypeSI.textChanged.connect(self.check_tab_3)
        self.tabWidget_3.currentWidget().lineEditZavNumber.textChanged.connect(self.check_tab_3)
        self.tabWidget_3.currentWidget().lineEditInventory.textChanged.connect(self.check_tab_3)

    def closeTab_SO (self, currentIndex):
        self.tabWidget_2.removeTab(currentIndex)
        self.tabWidget_2.setCurrentIndex(self.tabWidget_2.count() - 2)
        if self.tabWidget_2.count() == 1:
            self.tabWidget_2.removeTab(currentIndex)
            self.toolBox.setItemText(2, 'Стандартные образцы, применяемые при поверке')
            self.toolBox.setCurrentIndex(0)
            self.label_24.setText("Необходимо заполнить хотя бы одно поле")
            self.comboBox.setEnabled(True)
            self.check_tab_3()
        self.check_tab_3()

    def closeTab_SI (self, currentIndex):
        self.tabWidget_3.removeTab(currentIndex)
        self.tabWidget_3.setCurrentIndex(self.tabWidget_3.count() - 2)
        if self.tabWidget_3.count() == 1:
            self.tabWidget_3.removeTab(currentIndex)
            self.toolBox.setItemText(4, 'СИ, применяемые при поверке')
            self.toolBox.setCurrentIndex(0)
            self.label_24.setText("Необходимо заполнить хотя бы одно поле")
            self.comboBox.setEnabled(True)
            self.check_tab_3()
        self.check_tab_3()
    #==========================
    #Тестирование табов на заполнение полей
    def test_filled_tabs(self):
        '''
        При переходе от одного таба к другому происходит проверка того таба, с которого пользователь ушел
        '''
        if self.tabCurrIndex == 0:
            self.indicator_1 = True
            self.check_tab_1()
        elif self.tabCurrIndex == 1:
            self.indicator_2 = True
            self.check_tab_2()
        elif self.tabCurrIndex == 2:
            self.indicator_3 = True
            self.check_tab_3()
        elif self.tabCurrIndex == 3:
            self.indicator_4 = True
            self.check_tab_4()
        self.tabCurrIndex = self.tabWidget.currentIndex()
    #=========================
    #Действия по нажатию на радиобаттоны, чекбоксы и комбобоксы
    def onClicked_type_SI(self):
        '''
        Выбор типа СИ
        '''
        if self.radioButton.isChecked():
            self.lineEdit.setEnabled(True)
            self.lineEdit_2.setEnabled(False)
            self.lineEdit_3.setEnabled(False)
            self.lineEdit_2.setStyleSheet("")
            self.lineEdit_3.setStyleSheet("")
        elif self.radioButton_2.isChecked():
            self.lineEdit.setEnabled(False)
            self.lineEdit_2.setEnabled(True)
            self.lineEdit_3.setEnabled(False)
            self.lineEdit.setStyleSheet("")
            self.lineEdit_3.setStyleSheet("")
        elif self.radioButton_3.isChecked():
            self.lineEdit.setEnabled(False)
            self.lineEdit_2.setEnabled(False)
            self.lineEdit_3.setEnabled(True)
            self.lineEdit.setStyleSheet("")
            self.lineEdit_2.setStyleSheet("")

    def onClicked_zavNumber(self):
        '''
        Выбор заводского номера или буквенно-цифрового обозначения
        '''
        if self.radioButton_4.isChecked():
            self.lineEdit_5.setEnabled(True)
            self.lineEdit_25.setEnabled(True)
            self.lineEdit_27.setEnabled(True)
            self.lineEdit_6.setEnabled(False)
            self.lineEdit_26.setEnabled(False)
            self.lineEdit_29.setEnabled(False)
            self.lineEdit_29.setStyleSheet("")
        elif self.radioButton_5.isChecked():
            self.lineEdit_6.setEnabled(True)
            self.lineEdit_26.setEnabled(True)
            self.lineEdit_29.setEnabled(True)
            self.lineEdit_5.setEnabled(False)
            self.lineEdit_25.setEnabled(False)
            self.lineEdit_27.setEnabled(False)
            self.lineEdit_27.setStyleSheet("")

    def onClicked_applic_inapplic(self):
        '''
        Выбор Пригодно/Непригодно СИ
        '''
        if self.radioButton_8.isChecked():
            self.label_9.setEnabled(True)
            self.lineEdit_12.setEnabled(True)
            self.checkBox_2.setEnabled(True)
            self.checkBox_3.setEnabled(True)
            self.lineEdit_13.setEnabled(False)
            self.lineEdit_13.setStyleSheet("")
            self.label_10.setEnabled(False)
            self.check_tab_2()
        else:
            self.check_tab_2()
            self.label_10.setEnabled(True)
            self.lineEdit_13.setEnabled(True)
            self.label_9.setEnabled(False)
            self.lineEdit_12.setEnabled(False)
            self.checkBox_2.setEnabled(False)
            self.checkBox_3.setEnabled(False)

    def onClicked_comboBox(self):
        '''
        Установка активности на вкладке Средства поверки при выборе методов поверки без применения средств поверки
        '''
        if self.comboBox.currentIndex() > 0:
            self.toolBox.setEnabled(False)
            self.label_24.setVisible(False)
            self.line_3.setVisible(False)
        else:
            self.toolBox.setEnabled(True)
            self.check_tab_3()

    def onClicked_checkBox_4(self):
        '''
        Установка активности поля Краткая хар-ка объема поверки
        '''
        if self.checkBox_4.isChecked():
            self.label_24.setEnabled(True)
            self.textEdit_3.setEnabled(True)
            self.check_tab_4()
        else:
            self.textEdit_3.setStyleSheet("")
            self.label_24.setEnabled(False)
            self.textEdit_3.setEnabled(False)
            self.textEdit_3.clear()
    #=============================
    #Сбор данных для дальнейшей сборки заявки в цикле
    def collecting_data(self):
        '''
        Функция создана с целью оптимизации процесса формирования файлов,
        т.к. единожды записывает все данные в переменные (self.body_part_1, self.body_part_2 - для записи изменяемой части зав. номера, self.body_part_3) 
        и далее в цикле уже подставляет готовые данные, вместо постоянного прохода по строкам и дозапись в переменную self.main_body
        '''

        self.body_part_1 = ''
        self.body_part_3 = ''

        #Первая часть формируемой заявки
        self.body_part_1 = f'<gost:result>\n'+ f'<gost:miInfo>\n' + f'<gost:singleMI>\n'

        if self.radioButton.isChecked():
            self.body_part_1 += f'<gost:mitypeNumber>{self.mitypeNumber.strip(" ")}</gost:mitypeNumber>\n'
        elif self.radioButton_2.isChecked():
            self.body_part_1 += f'<gost:crtmitypeTitle>{self.mitypeNumber.strip(" ")}</gost:crtmitypeTitle>\n'
        elif self.radioButton_3.isChecked():
            self.body_part_1 += f'<gost:milmitypeTitle>{self.mitypeNumber.strip(" ")}</gost:milmitypeTitle>\n'

        #Третья часть формируемой заявки
        if self.manufactureYear != '':
            self.body_part_3 += f'<gost:manufactureYear>{self.manufactureYear}</gost:manufactureYear>\n'

        self.body_part_3 += f'<gost:modification>{self.modification.strip(" ")}</gost:modification>\n'

        self.body_part_3 += f'</gost:singleMI>\n'
        self.body_part_3 += f'</gost:miInfo>\n'
        self.body_part_3 += f'<gost:signCipher>{self.signCipher.strip(" ")}</gost:signCipher>\n'
        self.body_part_3 += f'<gost:miOwner>{self.miOwner.strip(" ")}</gost:miOwner>\n'

        self.body_part_3 += f'<gost:vrfDate>{self.vrfDate}</gost:vrfDate>\n'

        if self.validDate != '':
            self.body_part_3 += f'<gost:validDate>{self.validDate}</gost:validDate>\n'

        if self.radioButton_6.isChecked():
            self.body_part_3 += f'<gost:type>1</gost:type>\n'
        else:
            self.body_part_3 += f'<gost:type>2</gost:type>\n'

        self.body_part_3 += f'<gost:calibration>{self.calibration}</gost:calibration>\n'
        if self.radioButton_8.isChecked():
            self.body_part_3 += f'<gost:applicable>\n'
            if self.stickerNum != '':
                self.body_part_3 += f'<gost:stickerNum>{self.stickerNum.strip(" ")}</gost:stickerNum>\n'
            self.body_part_3 += f'<gost:signPass>{self.signPass}</gost:signPass>\n'
            self.body_part_3 += f'<gost:signMi>{self.signMi}</gost:signMi>\n'
            self.body_part_3 += f'</gost:applicable>\n'
        else:
            self.body_part_3 += f'<gost:inapplicable>\n'
            self.body_part_3 += f'<gost:reasons>{self.reasons.strip(" ")}</gost:reasons>\n'
            self.body_part_3 += f'</gost:inapplicable>\n'

        self.body_part_3 += f'<gost:docTitle>{self.method.strip(" ")}</gost:docTitle>\n'

        if self.metrologist != '':
            self.body_part_3 += f'<gost:metrologist>{self.metrologist.strip(" ")}</gost:metrologist>\n'

        self.body_part_3 += f'<gost:means>\n'

        if self.comboBox.currentIndex() == 0:
            if self.npe_number != '':
                text = self.npe_number.strip(' ')
                text = text.split(';')
                self.body_part_3 += f'<gost:npe>\n'
                for t in text:
                    if t != '' and not t.isspace():
                        self.body_part_3 += f'<gost:number>{t.strip(" ")}</gost:number>\n'
                self.body_part_3 += f'</gost:npe>\n'

            if self.uve_number != '':
                text = self.uve_number.strip(' ')
                text = text.split(';')
                self.body_part_3 += f'<gost:uve>\n'
                for t in text:
                    if t != '' and not t.isspace():
                        self.body_part_3 += f'<gost:number>{t.strip(" ")}</gost:number>\n'
                self.body_part_3 += f'</gost:uve>\n'

            if self.tabWidget_2.count() > 1:
                self.body_part_3 += f'<gost:ses>\n'
                for i in range(self.tabWidget_2.count() - 1):
                    self.body_part_3 += F'<gost:se>\n'
                    self.body_part_3 += f'<gost:typeNum>{self.tabWidget_2.widget(i).lineEditType.text().strip(" ")}</gost:typeNum>\n'
                    self.body_part_3 += f'<gost:manufactureYear>{self.tabWidget_2.widget(i).spinBoxManufYear.value()}</gost:manufactureYear>\n'
                    if self.tabWidget_2.widget(i).lineEditSerialNumber.text() != '' and not self.tabWidget_2.widget(i).lineEditSerialNumber.text().isspace():
                        self.body_part_3 += f'<gost:manufactureNum>{self.tabWidget_2.widget(i).lineEditSerialNumber.text().strip(" ")}</gost:manufactureNum>\n'
                    if self.tabWidget_2.widget(i).lineEditSpecifications.text() != '' and not self.tabWidget_2.widget(i).lineEditSpecifications.text().isspace():
                        self.body_part_3 += f'<gost:metroChars>{self.tabWidget_2.widget(i).lineEditSpecifications.text().strip(" ")}</gost:metroChars>\n'
                    self.body_part_3 += F'</gost:se>\n'
                self.body_part_3 += f'</gost:ses>\n'

            if self.mieta_number != '':
                text = self.mieta_number.strip(' ')
                text = text.split(';')
                self.body_part_3 += f'<gost:mieta>\n'
                for t in text:
                    if t != '' and not t.isspace():
                        self.body_part_3 += f'<gost:number>{t.strip(" ")}</gost:number>\n'
                self.body_part_3 += f'</gost:mieta>\n'

            if self.tabWidget_3.count() > 1:
                self.body_part_3 += f'<gost:mis>\n'
                for i in range(self.tabWidget_3.count() - 1):
                    self.body_part_3 += F'<gost:mi>\n'
                    self.body_part_3 += f'<gost:typeNum>{self.tabWidget_3.widget(i).lineEditTypeSI.text().strip(" ")}</gost:typeNum>\n'
                    if self.tabWidget_3.widget(i).lineEditZavNumber.text() != '':
                        self.body_part_3 += f'<gost:manufactureNum>{self.tabWidget_3.widget(i).lineEditZavNumber.text().strip(" ")}</gost:manufactureNum>\n'
                    elif self.tabWidget_3.widget(i).lineEditInventory.text() != '':
                        self.body_part_3 += f'<gost:inventoryNum>{self.tabWidget_3.widget(i).lineEditInventory.text().strip(" ")}</gost:inventoryNum>\n'
                    self.body_part_3 += F'</gost:mi>\n'
                self.body_part_3 += f'</gost:mis>\n'

            if self.reagent_number != '':
                text = self.reagent_number.strip(' ')
                text = text.split(';')
                self.body_part_3 += f'<gost:reagent>\n'
                for t in text:
                    if t != '' and not t.isspace():
                        self.body_part_3 += f'<gost:number>{t.strip(" ")}</gost:number>\n'
                self.body_part_3 += f'</gost:reagent>\n'

        else:
            self.body_part_3 += f'<gost:oMethod>{self.oMethod}</gost:oMethod>\n'

        self.body_part_3 += f'</gost:means>\n'

        self.body_part_3 += f'<gost:conditions>\n'
        self.body_part_3 += f'<gost:temperature>{self.temperature.strip(" ")} °C</gost:temperature>\n'
        self.body_part_3 += f'<gost:pressure>{self.pressure.strip(" ")} кПа</gost:pressure>\n'
        self.body_part_3 += f'<gost:hymidity>{self.hymidity.strip(" ")} %</gost:hymidity>\n'
        if self.other != '':
            self.body_part_3 += f'<gost:other>{self.other.strip(" ")}</gost:other>\n'
        self.body_part_3 += f'</gost:conditions>\n'

        if self.structure != '':
            self.body_part_3 += f'<gost:structure>{self.structure.strip(" ")}</gost:structure>\n'

        if self.checkBox_4.isChecked():
            self.body_part_3 += f'<gost:brief_procedure>\n'
            self.body_part_3 += f'<gost:characteristics>{self.characteristics.strip(" ")}</gost:characteristics>\n'
            self.body_part_3 += f'</gost:brief_procedure>\n'

        if self.additional_info != '':
            self.body_part_3 += f'<gost:additional_info>{self.additional_info.strip(" ")}</gost:additional_info>\n'

        self.body_part_3 += f'</gost:result>\n'
    #=============================
    def applic_constructor(self, filepath, result, part, counter_zav):
        '''
        Сборка записи о поверке и сохранение данных в файл
        '''
        date_stamp = datetime.now().strftime("%Y%m%d%H%M")

        #Название файла
        name_of_file = date_stamp + '_' + self.mitypeNumber.strip(' ') + '_part_' + str(part) + '_notes_' + str(result) + '_cifer_' + self.signCipher.strip(' ') + '.xml'

        #Путь сохранения файла
        FileFullPath = os.path.join(filepath, name_of_file)

        with open (FileFullPath, 'w', encoding='utf-8') as sample:

            header_1 = f'<?xml version="1.0" encoding="utf-8" ?>\n'
            header_comment_1 = f'<!--\n'
            header_comment_2 = f'Данный xml-файл создан при помощи ПО "Генератор заявок для партий СИ"\n'
            header_comment_3 = f'{version}\n'#Версия ПО
            header_comment_4 = f'-->\n'
            header_2 = f'<gost:application xmlns:gost="urn://fgis-arshin.gost.ru/module-verifications/import/2020-06-19">\n'
            header = header_1 + header_comment_1 + header_comment_2 + header_comment_3 + header_comment_4 + header_2
            sample.write(header)

        for n in range(result):
            #Основное тело записи о поверке
            self.main_body = ''
            self.body_part_2 = ''

            manufactureNum = self.prefix_zav_number.lstrip(' ') + str(counter_zav).zfill(self.zav_len) + self.tail_zav_number.rstrip(' ')

            #Вторая часть формируемой заявки
            if self.radioButton_4.isChecked():
                self.body_part_2 += f'<gost:manufactureNum>{manufactureNum}</gost:manufactureNum>\n'
            else:
                self.body_part_2 += f'<gost:inventoryNum>{manufactureNum}</gost:inventoryNum>\n'

            with open (FileFullPath, 'a', encoding='utf-8') as sample_body:
                self.main_body += self.body_part_1
                self.main_body += self.body_part_2
                self.main_body += self.body_part_3

                sample_body.write(self.main_body)

                counter_zav += 1

        with open (FileFullPath, 'a', encoding='utf-8') as sample:
            footer = f'</gost:application>\n'
            sample.write(footer)
            #=========================

        return counter_zav
    #=============================
    #Проверка что введенное значение в поле Заводской номер/БЦО является числом
    def check_zav_number_is_int(self, lineedit):
        try:
            self.counter_zav_number = int(self.counter_zav_number)
        except ValueError:
            if lineedit == self.lineEdit_27:
                self.lineEdit_27.setStyleSheet(style_line)
            elif lineedit == self.lineEdit_29:
                self.lineEdit_29.setStyleSheet(style_line)
    #=============================
    #Проверка таб 1
    def check_tab_1(self):
        #Тип СИ
        if self.radioButton.isChecked():
            self.mitypeNumber = self.lineEdit.text()
        elif self.radioButton_2.isChecked():
            self.mitypeNumber = self.lineEdit_2.text()
        elif self.radioButton_3.isChecked():
            self.mitypeNumber = self.lineEdit_3.text()
        #Модификация СИ
        self.modification = self.lineEdit_4.text()
        #Дата производства СИ
        self.manufactureYear = self.spinBox.text()
        if self.manufactureYear == '-':
            self.manufactureYear = ''
        else:
            self.manufactureYear = int(self.spinBox.text())
        #Заводской номер СИ
        if self.radioButton_4.isChecked():
            self.prefix_zav_number = self.lineEdit_5.text()
            self.counter_zav_number = self.lineEdit_27.text()
            self.zav_len = len(self.counter_zav_number.strip(' '))
            if self.counter_zav_number != '':
                self.check_zav_number_is_int(self.lineEdit_27)
            self.tail_zav_number = self.lineEdit_25.text()
        elif self.radioButton_5.isChecked():
            self.prefix_zav_number = self.lineEdit_6.text()
            self.counter_zav_number = self.lineEdit_29.text()
            self.zav_len = len(self.counter_zav_number.strip(' '))
            if self.counter_zav_number != '':
                self.check_zav_number_is_int(self.lineEdit_29)
            self.tail_zav_number = self.lineEdit_26.text()

        if self.indicator_1 == False:
            self.universal_fields_checker_with_sender()
            if self.mitypeNumber != '' and self.modification != '' and type(self.counter_zav_number) is int:
                self.count_1 = 1
            else:
                self.count_1 = 0

        else:
            field_tab_1 = {'mitypeNumber': [self.mitypeNumber, self.lineEdit, self.line],
                           'crtmitypeTitle': [self.mitypeNumber, self.lineEdit_2, self.line],
                           'milmitypeTitle': [self.mitypeNumber, self.lineEdit_3, self.line],
                           'self.modification': [self.modification, self.lineEdit_4, self.line],
                           'self.counter_zav_number': [str(self.counter_zav_number), self.lineEdit_27, self.line],
                           'self.counter_inv_number': [str(self.counter_zav_number), self.lineEdit_29, self.line]}

            if self.radioButton_4.isChecked():
                self.check_zav_number_is_int(self.lineEdit_27)
            elif self.radioButton_5.isChecked():
                self.check_zav_number_is_int(self.lineEdit_29)

            self.universal_fields_checker(field_tab_1)

            if self.mitypeNumber != '' and self.modification != '' and type(self.counter_zav_number) is int:
                self.line.setVisible(False)
                self.count_1 = 1
            else:
                self.line.setVisible(True)
                self.count_1 = 0

        self.start_to_create_application()
    #=============================
    #Проверка таб 2
    def check_tab_2(self):
        #Условный шифр знака поверки
        signCipher = self.lineEdit_7.text()
        self.signCipher = signCipher.upper()
        #Владелец СИ
        self.miOwner = self.lineEdit_8.text()
        #Методика поверки
        self.method = self.lineEdit_11.text()
        #Ф.И.О. поверителя
        self.metrologist = self.lineEdit_14.text()
        #Результаты калибровки (true/false)
        calibration = f'{self.checkBox.isChecked()}'
        self.calibration = calibration.lower()
        #Номер наклейки
        self.stickerNum = self.lineEdit_12.text()
        #Знак поверки в паспорте (true/false)
        signPass = f'{self.checkBox_2.isChecked()}'
        self.signPass = signPass.lower()
        #Знак поверки на СИ (true/false)
        signMi = f'{self.checkBox_3.isChecked()}'
        self.signMi = signMi.lower()
        #Причина непригодности
        self.reasons = self.lineEdit_13.text()

        if self.indicator_2 == False:
            self.universal_fields_checker_with_sender()

            if (self.radioButton_8.isChecked() and self.method != '' and self.signCipher != '' and self.miOwner != '' and self.vrfDate != '') or (self.radioButton_9.isChecked() and self.reasons != '' and self.method != '' and self.signCipher != '' and self.miOwner != '' and self.vrfDate != ''):
                self.count_2 = 1
                if self.validDate != '' and self.vrfDate == self.validDate:
                    self.label_43.setVisible(True)
                    self.label_43.setText('Даты не могут быть одинаковыми')
                    self.line_2.setVisible(True)
                    self.count_2 = 0
                elif self.validDate != '' and self.vrfDate > self.validDate:
                    self.label_43.setVisible(True)
                    self.label_43.setText('Окончание действия поверки не может наступать раньше ее проведения')
                    self.line_2.setVisible(True)
                    self.count_2 = 0
                else:
                    self.label_43.setVisible(False)
                    self.line_2.setVisible(False)
                    self.count_2 = 1
            else:
                self.count_2 = 0
        else:
            field_tab_2 = {'self.method': [self.method, self.lineEdit_11, self.line_2],
                           'self.vrfDate':[self.vrfDate, self.lineEdit_9, self.line_2],
                           'self.signCipher': [self.signCipher, self.lineEdit_7, self.line_2],
                           'self.miOwner': [self.miOwner, self.lineEdit_8, self.line_2],
                           'self.reasons': [self.reasons, self.lineEdit_13, self.line_2]}

            self.universal_fields_checker(field_tab_2)

            if (self.radioButton_8.isChecked() and self.method != '' and self.signCipher != '' and self.miOwner != '' and self.vrfDate != '') or (self.radioButton_9.isChecked() and self.reasons != '' and self.method != '' and self.signCipher != '' and self.miOwner != '' and self.vrfDate != ''):
                self.line_2.setVisible(False)
                self.count_2 = 1
                if self.validDate != '' and self.vrfDate == self.validDate:
                    self.label_43.setVisible(True)
                    self.label_43.setText('Даты не могут быть одинаковыми')
                    self.line_2.setVisible(True)
                    self.count_2 = 0
                elif self.validDate != '' and self.vrfDate > self.validDate:
                    self.label_43.setVisible(True)
                    self.label_43.setText('Окончание действия поверки не может наступать раньше ее проведения')
                    self.line_2.setVisible(True)
                    self.count_2 = 0
                else:
                    self.label_43.setVisible(False)
                    self.line_2.setVisible(False)
                    self.count_2 = 1
            else:
                self.line_2.setVisible(True)
                self.count_2 = 0

        self.start_to_create_application()
    #=============================
    #Проверка таб 3
    def check_tab_3(self):
        #ГПЭ
        self.npe_number = self.lineEdit_15.text()
        #Эталоны
        self.uve_number = self.lineEdit_16.text()
        #СИ, применяемые в качестве эталонов
        self.mieta_number = self.lineEdit_17.text()
        #Вещества (материалы)
        self.reagent_number = self.lineEdit_18.text()
        #Методы поверки без применения средств поверки
        self.oMethod = self.comboBox.currentIndex()

        if self.comboBox.currentIndex() == 0:
            if self.npe_number != '' or self.uve_number != '' or self.tabWidget_2.count() > 0 or self.mieta_number != '' or self.tabWidget_3.count() > 0 or self.reagent_number != '':
                self.line_3.setVisible(False)
                self.label_24.setVisible(False)
                self.comboBox.setEnabled(False)
                self.count_3 = 1
                self.count_3_1 = True
                self.count_3_2 = True
            else:
                self.comboBox.setEnabled(True)
                self.line_3.setVisible(True)
                self.label_24.setVisible(True)
                self.comboBox.setEnabled(True)
                self.count_3 = 0
                self.count_3_1 = False
                self.count_3_2 = False

            # #Проверка: Если создана вкладка СО, применяемые при поверке.
            if self.tabWidget_2.count() > 0:
                for i in range(self.tabWidget_2.count() - 1):
                    if self.tabWidget_2.widget(i).lineEditType.text() == '' or self.tabWidget_2.widget(i).lineEditType.text().isspace():
                        self.tabWidget_2.widget(i).lineEditType.setStyleSheet(style_line)
                        self.nb_SO.setEnabled(False)
                        self.line_3.setVisible(True)
                        self.label_24.setVisible(True)
                        self.label_24.setText("Необходимо проверить вкладку Стандартные образцы, применяемые при поверке")
                        self.tabWidget_2.setTabText(i, '!Образец!')
                        self.count_3_1 = False
                        self.start_to_create_application()
                        break
                    else:
                        self.tabWidget_2.widget(i).lineEditType.setStyleSheet('')
                        self.tabWidget_2.setTabText(i, 'Образец')
                        self.nb_SO.setEnabled(True)
                        self.line_3.setVisible(False)
                        self.label_24.setVisible(False)
                        self.count_3_1 = True
                        self.start_to_create_application()

            #Проверка: Если создана вкладка СИ, применяемые при поверке.
            if self.tabWidget_3.count() > 0:
                for i in range(self.tabWidget_3.count() - 1):
                    if self.tabWidget_3.widget(i).lineEditTypeSI.text() == '' or self.tabWidget_3.widget(i).lineEditTypeSI.text().isspace():
                        self.tabWidget_3.widget(i).lineEditTypeSI.setStyleSheet(style_line)
                        self.nb_SI.setEnabled(False)
                        self.line_3.setVisible(True)
                        self.label_24.setVisible(True)
                        self.label_24.setText("Необходимо проверить вкладку СИ, применяемые при поверке")
                        self.tabWidget_3.setTabText(i, '!СИ!')
                        self.count_3_2 = False
                        self.start_to_create_application()
                        break
                    else:
                        self.tabWidget_3.widget(i).lineEditZavNumber.setStyleSheet('')
                        self.tabWidget_3.widget(i).lineEditInventory.setStyleSheet('')
                        self.tabWidget_3.widget(i).lineEditTypeSI.setStyleSheet('')
                        self.nb_SI.setEnabled(True)
                        self.line_3.setVisible(False)
                        self.label_24.setVisible(False)
                        self.tabWidget_3.setTabText(i, 'СИ')
                        self.count_3_2 = True
                        self.start_to_create_application()
                        #Если заполнено поле Тип СИ, то проверка заполнения зав. № или буквенно-цифрового обозначения
                        if self.tabWidget_3.widget(i).lineEditTypeSI.text() != '' and (self.tabWidget_3.widget(i).lineEditZavNumber.text() == '' and self.tabWidget_3.widget(i).lineEditInventory.text() == ''):
                            self.tabWidget_3.widget(i).lineEditInventory.setEnabled(True)
                            self.tabWidget_3.widget(i).lineEditZavNumber.setEnabled(True)
                            self.tabWidget_3.widget(i).lineEditZavNumber.setStyleSheet(style_line)
                            self.tabWidget_3.widget(i).lineEditInventory.setStyleSheet(style_line)
                            self.nb_SI.setEnabled(False)
                            self.line_3.setVisible(True)
                            self.label_24.setVisible(True)
                            self.label_24.setText("Необходимо заполнить либо буквенно-цифровое обозначение, либо заводской номер")
                            self.tabWidget_3.setTabText(i, '!СИ!')
                            self.count_3_2 = False
                            self.start_to_create_application()
                            break
                        if self.tabWidget_3.widget(i).lineEditZavNumber.text() != '':
                            self.tabWidget_3.widget(i).lineEditInventory.setEnabled(False)
                        elif self.tabWidget_3.widget(i).lineEditInventory.text() != '':
                            self.tabWidget_3.widget(i).lineEditZavNumber.setEnabled(False)

            if self.count_3_1 and self.count_3_2:
                self.count_3 = 1
            else:
                self.line_3.setVisible(True)
                self.label_24.setVisible(True)
                self.count_3 = 0

        else:
            self.line_3.setVisible(False)
            self.label_24.setVisible(False)
            self.count_3 = 1

        self.start_to_create_application()
    #=============================
    #Проверка таб 4
    def check_tab_4(self):
        #Условия проведения поверки
        self.temperature = self.lineEdit_19.text()
        self.pressure = self.lineEdit_20.text()
        self.hymidity = self.lineEdit_21.text()
        #Другие факторы
        self.other = self.lineEdit_28.text()
        #Состав СИ, представленного на поверку
        self.structure = self.textEdit_2.toPlainText()
        #Краткая характеристика объема поверки
        self.characteristics = self.textEdit_3.toPlainText()
        #Прочие сведения
        self.additional_info = self.textEdit_4.toPlainText()

        if self.indicator_4 == False:
            self.universal_fields_checker_with_sender()
            if self.checkBox_4.checkState() == 0 and self.temperature != '' and self.pressure != '' and self.hymidity != '':
                self.count_4 = 1
            elif self.checkBox_4.isChecked() and self.characteristics != '' and self.temperature != '' and self.pressure != '' and self.hymidity != '':
                self.count_4 = 1
            else:
                self.count_4 = 0
        else:
            field_tab_4 = {'self.temperature': [self.temperature, self.lineEdit_19, self.line_4],
                        'self.pressure': [self.pressure, self.lineEdit_20, self.line_4],
                        'self.hymidity': [self.hymidity, self.lineEdit_21, self.line_4],
                        'self.characteristics': [self.characteristics, self.textEdit_3, self.line_4]}

            self.universal_fields_checker(field_tab_4)

            if self.checkBox_4.checkState() == 0 and self.temperature != '' and self.pressure != '' and self.hymidity != '':
                self.line_4.setVisible(False)
                self.count_4 = 1
            elif self.checkBox_4.isChecked() and self.characteristics != '' and self.temperature != '' and self.pressure != '' and self.hymidity != '':
                self.line_4.setVisible(False)
                self.count_4 = 1
            else:
                self.line_4.setVisible(True)
                self.count_4 = 0

        self.start_to_create_application()
    #=============================
    def universal_fields_checker(self, field_tab):
        '''
        Универсальная функция проверки заполнения полей использующая словари с указанными полями (переменные, виджеты, сигнальные линии над вкладками)
        '''
        for field in field_tab.keys():
            required_field = field_tab[field][1]
            alert_field = field_tab[field][2]
            #Проход циклом по всем обязательным полям, выявление незаполненных обязательных полей
            if (field != 'self.reasons' and field != 'self.characteristics' and field != 'mitypeNumber' and field != 'crtmitypeTitle' and field != 'milmitypeTitle' and field != 'self.counter_zav_number' and field != 'self.counter_inv_number') and field_tab[field][0] == '' or field_tab[field][0].isspace():
                required_field.setStyleSheet(style_line)
                alert_field.setVisible(True)
            elif (field == 'self.reasons' and self.radioButton_9.isChecked()) and (field_tab[field][0] == '' or field_tab[field][0].isspace()):
                required_field.setStyleSheet(style_line)
                alert_field.setVisible(True)
            elif (field == 'self.characteristics' and self.checkBox_4.isChecked()) and (field_tab[field][0] == '' or field_tab[field][0].isspace()):
                required_field.setStyleSheet(style_line)
                alert_field.setVisible(True)
            elif (field == 'mitypeNumber' and self.radioButton.isChecked()) and (field_tab[field][0] == '' or field_tab[field][0].isspace()):
                required_field.setStyleSheet(style_line)
                alert_field.setVisible(True)
            elif (field == 'crtmitypeTitle' and self.radioButton_2.isChecked()) and (field_tab[field][0] == '' or field_tab[field][0].isspace()):
                required_field.setStyleSheet(style_line)
                alert_field.setVisible(True)
            elif (field == 'milmitypeTitle' and self.radioButton_3.isChecked()) and (field_tab[field][0] == '' or field_tab[field][0].isspace()):
                required_field.setStyleSheet(style_line)
                alert_field.setVisible(True)
            elif (field == 'self.counter_zav_number' and self.radioButton_4.isChecked()) and (field_tab[field][0] == '' or field_tab[field][0].isspace() or not type(self.counter_zav_number) is int):
                required_field.setStyleSheet(style_line)
                alert_field.setVisible(True)
            elif (field == 'self.counter_inv_number' and self.radioButton_5.isChecked()) and (field_tab[field][0] == '' or field_tab[field][0].isspace() or not type(self.counter_zav_number) is int):
                required_field.setStyleSheet(style_line)
                alert_field.setVisible(True)
            else:
                required_field.setStyleSheet('')
                alert_field.setVisible(False)
    #=============================
    def universal_fields_checker_with_sender(self):
        '''
        Универсальная функция проверки заполнения полей использующая sender в качестве источника сигнала (sender получает данные от разных переменных)
        '''
        sender = self.sender()
        is_lineEdit = isinstance(sender, QtWidgets.QLineEdit)
        is_textEdit = isinstance(sender, QtWidgets.QTextEdit)
        if is_lineEdit and (sender.text() == '' or sender.text().isspace()):
            sender.setStyleSheet(style_line)
        elif (is_textEdit and self.checkBox_4.isChecked()) and (sender.toPlainText() == '' or sender.toPlainText().isspace()):
            sender.setStyleSheet(style_line)
        else:
            sender.setStyleSheet('')

        if sender == self.lineEdit_27 and not type(self.counter_zav_number) is int:
            self.check_zav_number_is_int(self.lineEdit_27)
            sender.setStyleSheet(style_line)
        elif sender == self.lineEdit_29 and not type(self.counter_zav_number) is int:
            self.check_zav_number_is_int(self.lineEdit_29)
            sender.setStyleSheet(style_line)
        if sender == self.lineEdit_10:
            sender.setStyleSheet('')
    #=============================
    def start_to_create_application(self):
        '''
        Функция проверяет все ли условия выполнены для допуска к формированию xml-файла
        '''
        self.result = 0
        self.result = self.count_1 + self.count_2 + self.count_3 + self.count_4

        if self.result == 4:
            self.pushButton.setText("Создать xml-файл")
            self.pushButton.setEnabled(True)
        else:
            self.pushButton.setText("Заполните форму")
            self.pushButton.setEnabled(False)
    #=============================
    def update_data(self):
        '''
        Обновление содержимого переменных (для случая, если после формирования файлов внесены изменения в необязательные поля,
        т.к. для этих полей нет проверки изменения содержимого на-лету)
        '''
        #Тип СИ
        if self.radioButton.isChecked():
            self.mitypeNumber = self.lineEdit.text()
        elif self.radioButton_2.isChecked():
            self.mitypeNumber = self.lineEdit_2.text()
        elif self.radioButton_3.isChecked():
            self.mitypeNumber = self.lineEdit_3.text()
        #Модификация СИ
        self.modification = self.lineEdit_4.text()
        #Дата производства СИ
        self.manufactureYear = self.spinBox.text()
        if self.manufactureYear == '-':
            self.manufactureYear = ''
        else:
            self.manufactureYear = int(self.spinBox.text())
        #Заводской номер СИ
        if self.radioButton_4.isChecked():
            self.prefix_zav_number = self.lineEdit_5.text()
            self.counter_zav_number = self.lineEdit_27.text()
            self.zav_len = len(self.counter_zav_number.strip(' '))
            if self.counter_zav_number != '':
                self.check_zav_number_is_int(self.lineEdit_27)
            self.tail_zav_number = self.lineEdit_25.text()
        elif self.radioButton_5.isChecked():
            self.prefix_zav_number = self.lineEdit_6.text()
            self.counter_zav_number = self.lineEdit_29.text()
            self.zav_len = len(self.counter_zav_number.strip(' '))
            if self.counter_zav_number != '':
                self.check_zav_number_is_int(self.lineEdit_29)
            self.tail_zav_number = self.lineEdit_26.text()
        #Условный шифр знака поверки
        signCipher = self.lineEdit_7.text()
        self.signCipher = signCipher.upper()
        #Владелец СИ
        self.miOwner = self.lineEdit_8.text()
        #Методика поверки
        self.method = self.lineEdit_11.text()
        #Ф.И.О. поверителя
        self.metrologist = self.lineEdit_14.text()
        #Результаты калибровки (true/false)
        calibration = f'{self.checkBox.isChecked()}'
        self.calibration = calibration.lower()
        #Номер наклейки
        self.stickerNum = self.lineEdit_12.text()
        #Знак поверки в паспорте (true/false)
        signPass = f'{self.checkBox_2.isChecked()}'
        self.signPass = signPass.lower()
        #Знак поверки на СИ (true/false)
        signMi = f'{self.checkBox_3.isChecked()}'
        self.signMi = signMi.lower()
        #Причина непригодности
        self.reasons = self.lineEdit_13.text()
        #ГПЭ
        self.npe_number = self.lineEdit_15.text()
        #Эталоны
        self.uve_number = self.lineEdit_16.text()
        #СИ, применяемые в качестве эталонов
        self.mieta_number = self.lineEdit_17.text()
        #Вещества (материалы)
        self.reagent_number = self.lineEdit_18.text()
        #Методы поверки без применения средств поверки
        self.oMethod = self.comboBox.currentIndex()
        #Условия проведения поверки
        self.temperature = self.lineEdit_19.text()
        self.pressure = self.lineEdit_20.text()
        self.hymidity = self.lineEdit_21.text()
        #Другие факторы
        self.other = self.lineEdit_28.text()
        #Состав СИ, представленного на поверку
        self.structure = self.textEdit_2.toPlainText()
        #Краткая характеристика объема поверки
        self.characteristics = self.textEdit_3.toPlainText()
        #Прочие сведения
        self.additional_info = self.textEdit_4.toPlainText()
    #=============================
    def create(self):
        self.tabWidget.setEnabled(False)
        self.pushButton.setText("Подготовка данных")
        #Обновление содержимого переменных
        self.update_data()
        #Сбор данных в переменные
        self.collecting_data()
        #Общее количество записей о поверках СИ
        TOTAL_RESULTS = int(self.spinBox_3.text())
        #Количество записей о поверках СИ в одной заявке (не более 5000 записей)
        RESULTS_IN_APP = int(self.spinBox_4.text())

        filepath = QtWidgets.QFileDialog.getExistingDirectory(self, "Каталог сохранения файлов")
        if filepath != '':
            parts = TOTAL_RESULTS // RESULTS_IN_APP # Вычисление количества заявок (Общее количество заявок делится без остатка на желаемое количество в одной заявке)
            if TOTAL_RESULTS % RESULTS_IN_APP != 0: # Если остаток от деления заявок на части не равен 0, то количество заявок увеличивается на 1.
                parts += 1

            set_progress = 0
            progress_value = 100 / (TOTAL_RESULTS / RESULTS_IN_APP)

            #Заводской номер СИ
            counter_zav_number = self.counter_zav_number
            self.hidePushButtonShowProgressBar()

            for j in range(parts):
                if TOTAL_RESULTS <= RESULTS_IN_APP:
                    zav = self.applic_constructor(filepath, TOTAL_RESULTS, j + 1, counter_zav_number)
                elif TOTAL_RESULTS > RESULTS_IN_APP:
                    zav = self.applic_constructor(filepath, RESULTS_IN_APP, j + 1, counter_zav_number)
                    TOTAL_RESULTS -= RESULTS_IN_APP
                counter_zav_number = zav
                QtWidgets.QApplication.processEvents()

                set_progress += progress_value
                if set_progress > 100:
                    set_progress = 100
                self.progressBar.setValue(round(set_progress))

            self.statusBar().showMessage('Формирование файлов завершено!')
            self.pushButton.setEnabled(False)
            self.pushButton.setText("Файл создан")
            self.pushButton.show()
            self.progressBar.close()
            self.statusTimer()

style_line = """
QLineEdit {
    border: 1px solid #ff0000;
    border-radius: 3px;
    background: #ffbcbc;
    selection-background-color: darkgray;
}
QTextEdit {
    border: 1px solid #ff0000;
    border-radius: 3px;
    background: #ffbcbc;
    selection-background-color: darkgray;
}
"""

qss = """
QToolBox::tab {
    background: #e6e6e6;
    border-radius: 3px;
    border: 1px solid #d8d8d8;
    color: #5f5f5f;
}

QToolBox::tab:selected {
    font: bold;
    color: black;
}

QTabBar::close-button {
    image: url(:/icons/close_red_3.png);
    subcontrol-position: right;
}
QTabBar::close-button:hover {
    image: url(:/icons/close_red_hover.png);
}
QTabBar::close-button:pressed {
    image: url(:/icons/close_red_clicked.png);
}

QWidget#page, 
QWidget#page_2, 
QWidget#page_3, 
QWidget#page_4, 
QWidget#page_5, 
QWidget#page_6 {
    background: white;
}

QWidget#widget_header {
    background: white;
    border-radius: 1px;
    border: 1px solid #b1b1b1;
}

QCalendarWidget QWidget#qt_calendar_navigationbar { 
    background-color: rgb(245, 245, 245); 
}

QCalendarWidget QAbstractItemView:enabled {
    font-size:12px;
    color:rgb(0, 0, 0);
    background-color:rgb(255, 255, 255);
    selection-background-color:rgb(0, 85, 255);
    selection-color: rgb(255, 255, 255);
}

QCalendarWidget QToolButton {
        color:rgb(0, 0, 0);
}
"""

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet(qss)
    Logo()
    window = main_window()
    window.show()
    sys.exit(app.exec_())