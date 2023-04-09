# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QColorDialog, QMessageBox, QGraphicsScene, QWidget
from PyQt5.QtGui import QPixmap, QColor, QPen
from PyQt5.QtCore import QPoint, QRect

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1269, 850)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(290, 0, 981, 821))
        self.graphicsView.setObjectName("graphicsView")
        self.color_label = QtWidgets.QLabel(self.centralwidget)
        self.color_label.setGeometry(QtCore.QRect(30, 130, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.color_label.setFont(font)
        self.color_label.setObjectName("color_label")
        self.but_color_def = QtWidgets.QPushButton(self.centralwidget)
        self.but_color_def.setGeometry(QtCore.QRect(0, 40, 281, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.but_color_def.setFont(font)
        self.but_color_def.setObjectName("but_color_def")
        self.color_indicate = QtWidgets.QLabel(self.centralwidget)
        self.color_indicate.setGeometry(QtCore.QRect(190, 130, 61, 41))
        self.color_indicate.setAutoFillBackground(False)
        self.color_indicate.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.color_indicate.setObjectName("color_indicate")
        self.but_color_own = QtWidgets.QPushButton(self.centralwidget)
        self.but_color_own.setGeometry(QtCore.QRect(0, 80, 281, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.but_color_own.setFont(font)
        self.but_color_own.setObjectName("but_color_own")
        self.but_color_bg = QtWidgets.QPushButton(self.centralwidget)
        self.but_color_bg.setGeometry(QtCore.QRect(0, 0, 281, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.but_color_bg.setFont(font)
        self.but_color_bg.setObjectName("but_color_bg")
        self.rad_can = QtWidgets.QRadioButton(self.centralwidget)
        self.rad_can.setGeometry(QtCore.QRect(10, 370, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.rad_can.setFont(font)
        self.rad_can.setObjectName("rad_can")
        self.rad_par = QtWidgets.QRadioButton(self.centralwidget)
        self.rad_par.setGeometry(QtCore.QRect(10, 400, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.rad_par.setFont(font)
        self.rad_par.setObjectName("rad_par")
        self.rad_br = QtWidgets.QRadioButton(self.centralwidget)
        self.rad_br.setGeometry(QtCore.QRect(10, 430, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.rad_br.setFont(font)
        self.rad_br.setObjectName("rad_br")
        self.rad_mid = QtWidgets.QRadioButton(self.centralwidget)
        self.rad_mid.setGeometry(QtCore.QRect(10, 460, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.rad_mid.setFont(font)
        self.rad_mid.setObjectName("rad_mid")
        self.rad_qt = QtWidgets.QRadioButton(self.centralwidget)
        self.rad_qt.setGeometry(QtCore.QRect(10, 490, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.rad_qt.setFont(font)
        self.rad_qt.setObjectName("rad_qt")
        self.line_centre = QtWidgets.QLineEdit(self.centralwidget)
        self.line_centre.setGeometry(QtCore.QRect(10, 200, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.line_centre.setFont(font)
        self.line_centre.setAlignment(QtCore.Qt.AlignCenter)
        self.line_centre.setObjectName("line_centre")
        self.lab_centre = QtWidgets.QLabel(self.centralwidget)
        self.lab_centre.setGeometry(QtCore.QRect(10, 160, 281, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lab_centre.setFont(font)
        self.lab_centre.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_centre.setObjectName("lab_centre")
        self.line_r = QtWidgets.QLineEdit(self.centralwidget)
        self.line_r.setGeometry(QtCore.QRect(10, 280, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.line_r.setFont(font)
        self.line_r.setText("")
        self.line_r.setAlignment(QtCore.Qt.AlignCenter)
        self.line_r.setObjectName("line_r")
        self.lab_rad = QtWidgets.QLabel(self.centralwidget)
        self.lab_rad.setGeometry(QtCore.QRect(10, 230, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lab_rad.setFont(font)
        self.lab_rad.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_rad.setObjectName("lab_rad")
        self.lab_a_b = QtWidgets.QLabel(self.centralwidget)
        self.lab_a_b.setGeometry(QtCore.QRect(150, 230, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lab_a_b.setFont(font)
        self.lab_a_b.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_a_b.setObjectName("lab_a_b")
        self.line_a_b = QtWidgets.QLineEdit(self.centralwidget)
        self.line_a_b.setGeometry(QtCore.QRect(150, 280, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.line_a_b.setFont(font)
        self.line_a_b.setText("")
        self.line_a_b.setAlignment(QtCore.Qt.AlignCenter)
        self.line_a_b.setObjectName("line_a_b")
        self.but_draw_sir = QtWidgets.QPushButton(self.centralwidget)
        self.but_draw_sir.setGeometry(QtCore.QRect(10, 310, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.but_draw_sir.setFont(font)
        self.but_draw_sir.setObjectName("but_draw_sir")
        self.but_draw_el = QtWidgets.QPushButton(self.centralwidget)
        self.but_draw_el.setGeometry(QtCore.QRect(150, 310, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.but_draw_el.setFont(font)
        self.but_draw_el.setObjectName("but_draw_el")
        self.line_sp_centre = QtWidgets.QLineEdit(self.centralwidget)
        self.line_sp_centre.setGeometry(QtCore.QRect(10, 560, 271, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.line_sp_centre.setFont(font)
        self.line_sp_centre.setAlignment(QtCore.Qt.AlignCenter)
        self.line_sp_centre.setObjectName("line_sp_centre")
        self.lab_sp_centre = QtWidgets.QLabel(self.centralwidget)
        self.lab_sp_centre.setGeometry(QtCore.QRect(10, 540, 271, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lab_sp_centre.setFont(font)
        self.lab_sp_centre.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_sp_centre.setObjectName("lab_sp_centre")
        self.but_color_sp_sir = QtWidgets.QPushButton(self.centralwidget)
        self.but_color_sp_sir.setGeometry(QtCore.QRect(10, 710, 121, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.but_color_sp_sir.setFont(font)
        self.but_color_sp_sir.setObjectName("but_color_sp_sir")
        self.but_draw_sp_el = QtWidgets.QPushButton(self.centralwidget)
        self.but_draw_sp_el.setGeometry(QtCore.QRect(160, 710, 121, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.but_draw_sp_el.setFont(font)
        self.but_draw_sp_el.setObjectName("but_draw_sp_el")
        self.line_r_max = QtWidgets.QLineEdit(self.centralwidget)
        self.line_r_max.setGeometry(QtCore.QRect(70, 590, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.line_r_max.setFont(font)
        self.line_r_max.setText("")
        self.line_r_max.setObjectName("line_r_max")
        self.line_r_min = QtWidgets.QLineEdit(self.centralwidget)
        self.line_r_min.setGeometry(QtCore.QRect(70, 620, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.line_r_min.setFont(font)
        self.line_r_min.setText("")
        self.line_r_min.setObjectName("line_r_min")
        self.lab_r_min = QtWidgets.QLabel(self.centralwidget)
        self.lab_r_min.setGeometry(QtCore.QRect(10, 590, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lab_r_min.setFont(font)
        self.lab_r_min.setObjectName("lab_r_min")
        self.lab_r_max = QtWidgets.QLabel(self.centralwidget)
        self.lab_r_max.setGeometry(QtCore.QRect(10, 620, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lab_r_max.setFont(font)
        self.lab_r_max.setObjectName("lab_r_max")
        self.line_r_step = QtWidgets.QLineEdit(self.centralwidget)
        self.line_r_step.setGeometry(QtCore.QRect(70, 650, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.line_r_step.setFont(font)
        self.line_r_step.setText("")
        self.line_r_step.setObjectName("line_r_step")
        self.lab_r_step = QtWidgets.QLabel(self.centralwidget)
        self.lab_r_step.setGeometry(QtCore.QRect(10, 650, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lab_r_step.setFont(font)
        self.lab_r_step.setObjectName("lab_r_step")
        self.lab_a_step = QtWidgets.QLabel(self.centralwidget)
        self.lab_a_step.setGeometry(QtCore.QRect(160, 650, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lab_a_step.setFont(font)
        self.lab_a_step.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lab_a_step.setObjectName("lab_a_step")
        self.line_a_min = QtWidgets.QLineEdit(self.centralwidget)
        self.line_a_min.setGeometry(QtCore.QRect(220, 590, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.line_a_min.setFont(font)
        self.line_a_min.setText("")
        self.line_a_min.setObjectName("line_a_min")
        self.line_a_step = QtWidgets.QLineEdit(self.centralwidget)
        self.line_a_step.setGeometry(QtCore.QRect(220, 650, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.line_a_step.setFont(font)
        self.line_a_step.setText("")
        self.line_a_step.setObjectName("line_a_step")
        self.line_a_max = QtWidgets.QLineEdit(self.centralwidget)
        self.line_a_max.setGeometry(QtCore.QRect(220, 620, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.line_a_max.setFont(font)
        self.line_a_max.setText("")
        self.line_a_max.setObjectName("line_a_max")
        self.lab_a_max = QtWidgets.QLabel(self.centralwidget)
        self.lab_a_max.setGeometry(QtCore.QRect(160, 620, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lab_a_max.setFont(font)
        self.lab_a_max.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lab_a_max.setObjectName("lab_a_max")
        self.lab_a_min = QtWidgets.QLabel(self.centralwidget)
        self.lab_a_min.setGeometry(QtCore.QRect(160, 590, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lab_a_min.setFont(font)
        self.lab_a_min.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lab_a_min.setObjectName("lab_a_min")
        self.line_s_a_b = QtWidgets.QLineEdit(self.centralwidget)
        self.line_s_a_b.setGeometry(QtCore.QRect(220, 680, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.line_s_a_b.setFont(font)
        self.line_s_a_b.setText("")
        self.line_s_a_b.setObjectName("line_s_a_b")
        self.lab_sp_a_b = QtWidgets.QLabel(self.centralwidget)
        self.lab_sp_a_b.setGeometry(QtCore.QRect(160, 680, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lab_sp_a_b.setFont(font)
        self.lab_sp_a_b.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lab_sp_a_b.setObjectName("lab_sp_a_b")
        self.but_clear = QtWidgets.QPushButton(self.centralwidget)
        self.but_clear.setGeometry(QtCore.QRect(10, 770, 271, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.but_clear.setFont(font)
        self.but_clear.setObjectName("but_clear")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1269, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Лабораторная работа #4"))
        self.color_label.setText(_translate("MainWindow", "Текущий цвет:"))
        self.but_color_def.setText(_translate("MainWindow", "Рисовать цветом по умолчанию"))
        self.color_indicate.setText(_translate("MainWindow", "    Color"))
        self.but_color_own.setText(_translate("MainWindow", "Рисовать своим цветом"))
        self.but_color_bg.setText(_translate("MainWindow", "Рисовать цветом фона"))
        self.rad_can.setText(_translate("MainWindow", "Каноническое уравнение"))
        self.rad_par.setText(_translate("MainWindow", "Параметрическое уравнение"))
        self.rad_br.setText(_translate("MainWindow", "Алгоритм Брезенхема"))
        self.rad_mid.setText(_translate("MainWindow", "Алгоритм средней точки"))
        self.rad_qt.setText(_translate("MainWindow", "Библиотечная реализация(Qt)"))
        self.lab_centre.setText(_translate("MainWindow", "Координаты центра"))
        self.lab_rad.setText(_translate("MainWindow", "Радиус\n"
                    "(окружность)"))
        self.lab_a_b.setText(_translate("MainWindow", "Расстояния a и b\n"
                    "(эллипс)"))
        self.but_draw_sir.setText(_translate("MainWindow", "Нарисовать\n"
                    "Окружность"))
        self.but_draw_el.setText(_translate("MainWindow", "Нарисовать\n"
                    "Эллипс"))
        self.lab_sp_centre.setText(_translate("MainWindow", "Координаты центра спектра"))
        self.but_color_sp_sir.setText(_translate("MainWindow", "Спектр\n"
                    "окружностей"))
        self.but_draw_sp_el.setText(_translate("MainWindow", "Спектр\n"
                    "эллипсов"))
        self.lab_r_min.setText(_translate("MainWindow", "R_min"))
        self.lab_r_max.setText(_translate("MainWindow", "R_max"))
        self.lab_r_step.setText(_translate("MainWindow", "Шаг R"))
        self.lab_a_step.setText(_translate("MainWindow", "Шаг a"))
        self.lab_a_max.setText(_translate("MainWindow", "a_max"))
        self.lab_a_min.setText(_translate("MainWindow", "a_min"))
        self.lab_sp_a_b.setText(_translate("MainWindow", "a/b"))
        self.but_clear.setText(_translate("MainWindow", "Очистить экран"))
