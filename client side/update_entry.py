# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'update-entry.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(572, 320)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 10, 57, 15))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(40, 170, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(40, 80, 57, 15))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.update_button = QtWidgets.QPushButton(Dialog)
        self.update_button.setGeometry(QtCore.QRect(90, 240, 141, 41))
        self.update_button.setObjectName("update_button")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(40, 120, 57, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.title_input = QtWidgets.QLineEdit(Dialog)
        self.title_input.setGeometry(QtCore.QRect(150, 70, 231, 31))
        self.title_input.setObjectName("title_input")
        self.login_input = QtWidgets.QLineEdit(Dialog)
        self.login_input.setGeometry(QtCore.QRect(150, 122, 231, 31))
        self.login_input.setObjectName("login_input")
        self.password_input = QtWidgets.QLineEdit(Dialog)
        self.password_input.setGeometry(QtCore.QRect(152, 162, 231, 31))
        self.password_input.setObjectName("password_input")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Update Enrtry"))
        self.label.setText(_translate("Dialog", "Update"))
        self.label_2.setText(_translate("Dialog", "Password"))
        self.label_3.setText(_translate("Dialog", "Title"))
        self.update_button.setText(_translate("Dialog", "Update"))
        self.label_4.setText(_translate("Dialog", "Login"))
