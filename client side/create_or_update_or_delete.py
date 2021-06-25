# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'create_or_update_or_delete.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(379, 402)
        self.update_button = QtWidgets.QPushButton(Dialog)
        self.update_button.setGeometry(QtCore.QRect(110, 110, 141, 51))
        self.update_button.setObjectName("update_button")
        self.delete_button = QtWidgets.QPushButton(Dialog)
        self.delete_button.setGeometry(QtCore.QRect(110, 190, 141, 51))
        self.delete_button.setObjectName("delete_button")
        self.create_button = QtWidgets.QPushButton(Dialog)
        self.create_button.setGeometry(QtCore.QRect(110, 30, 141, 51))
        self.create_button.setObjectName("create_button")
        self.cancel_button = QtWidgets.QPushButton(Dialog)
        self.cancel_button.setGeometry(QtCore.QRect(110, 270, 141, 51))
        self.cancel_button.setObjectName("cancel_button")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.update_button.setText(_translate("Dialog", "Update this entry"))
        self.delete_button.setText(_translate("Dialog", "Delete this entry"))
        self.create_button.setText(_translate("Dialog", "Create new entry"))
        self.cancel_button.setText(_translate("Dialog", "Cancel"))

