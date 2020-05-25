# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/gs/devel/bulk_email/ConfigDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(435, 317)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.leUsername = QtWidgets.QLineEdit(Dialog)
        self.leUsername.setObjectName("leUsername")
        self.gridLayout.addWidget(self.leUsername, 4, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 7, 1, 1, 1)
        self.leSenderName = QtWidgets.QLineEdit(Dialog)
        self.leSenderName.setObjectName("leSenderName")
        self.gridLayout.addWidget(self.leSenderName, 0, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 6, 0, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.sbPort = QtWidgets.QSpinBox(Dialog)
        self.sbPort.setMaximum(65535)
        self.sbPort.setProperty("value", 25)
        self.sbPort.setObjectName("sbPort")
        self.gridLayout.addWidget(self.sbPort, 3, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)
        self.leServer = QtWidgets.QLineEdit(Dialog)
        self.leServer.setObjectName("leServer")
        self.gridLayout.addWidget(self.leServer, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)
        self.leSenderEmail = QtWidgets.QLineEdit(Dialog)
        self.leSenderEmail.setObjectName("leSenderEmail")
        self.gridLayout.addWidget(self.leSenderEmail, 1, 1, 1, 1)
        self.cbSecurity = QtWidgets.QComboBox(Dialog)
        self.cbSecurity.setObjectName("cbSecurity")
        self.cbSecurity.addItem("")
        self.cbSecurity.setItemText(0, "")
        self.cbSecurity.addItem("")
        self.cbSecurity.addItem("")
        self.gridLayout.addWidget(self.cbSecurity, 6, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 8, 0, 1, 2)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.lePassword = QtWidgets.QLineEdit(Dialog)
        self.lePassword.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.lePassword.setObjectName("lePassword")
        self.gridLayout.addWidget(self.lePassword, 5, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.leSenderName, self.leSenderEmail)
        Dialog.setTabOrder(self.leSenderEmail, self.leServer)
        Dialog.setTabOrder(self.leServer, self.sbPort)
        Dialog.setTabOrder(self.sbPort, self.leUsername)
        Dialog.setTabOrder(self.leUsername, self.lePassword)
        Dialog.setTabOrder(self.lePassword, self.cbSecurity)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Impostazioni"))
        self.label_2.setText(_translate("Dialog", "SMTP User"))
        self.label_5.setText(_translate("Dialog", "Sicurezza"))
        self.label.setText(_translate("Dialog", "SMTP Server"))
        self.label_6.setText(_translate("Dialog", "Nome Mittente"))
        self.label_3.setText(_translate("Dialog", "SMTP Password"))
        self.cbSecurity.setItemText(1, _translate("Dialog", "SSL"))
        self.cbSecurity.setItemText(2, _translate("Dialog", "TLS"))
        self.label_4.setText(_translate("Dialog", "SMTP Port"))
        self.label_7.setText(_translate("Dialog", "E-mail Mittente"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
