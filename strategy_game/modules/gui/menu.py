# Form implementation generated from reading ui file 'C:\Users\gilya\Projects\PyCharm\ORIS-tasks\strategy_game\modules\gui\menu.ui'
#
# Created by: PyQt6 UI code generator 6.8.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Menu(object):
    def setupUi(self, Menu):
        Menu.setObjectName("Menu")
        Menu.resize(500, 300)
        Menu.setMinimumSize(QtCore.QSize(500, 300))
        Menu.setStyleSheet("#Menu {background-color: #DFE0E2}\n"
"\n"
"QFrame {\n"
"    background-color: #C9CBCF;\n"
"    border-radius: 20px;\n"
"}\n"
"\n"
"QLineEdit, QPushButton {\n"
"    color: black;\n"
"    border-radius: 10px;\n"
"    padding: 10px;\n"
"    font-size: 14px;\n"
"}\n"
"QLineEdit {background-color: white}\n"
"QLineEdit[highlight-incorrect=true] {border: 1px solid red}\n"
"\n"
"QPushButton {background-color: #85D2FF}\n"
"QPushButton:hover {background-color: #5CC3FF}\n"
"QPushButton:disabled {\n"
"    background-color: #D6F0FF;\n"
"    color: #40404F;\n"
"}")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Menu)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_menu = QtWidgets.QFrame(parent=Menu)
        self.frame_menu.setMinimumSize(QtCore.QSize(300, 200))
        self.frame_menu.setMaximumSize(QtCore.QSize(300, 200))
        self.frame_menu.setObjectName("frame_menu")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_menu)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setHorizontalSpacing(25)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        self.btn_host = QtWidgets.QPushButton(parent=self.frame_menu)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_host.sizePolicy().hasHeightForWidth())
        self.btn_host.setSizePolicy(sizePolicy)
        self.btn_host.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_host.setObjectName("btn_host")
        self.gridLayout.addWidget(self.btn_host, 3, 0, 1, 1)
        self.btn_connect = QtWidgets.QPushButton(parent=self.frame_menu)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_connect.sizePolicy().hasHeightForWidth())
        self.btn_connect.setSizePolicy(sizePolicy)
        self.btn_connect.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_connect.setObjectName("btn_connect")
        self.gridLayout.addWidget(self.btn_connect, 3, 1, 1, 1)
        self.input_address = QtWidgets.QLineEdit(parent=self.frame_menu)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_address.sizePolicy().hasHeightForWidth())
        self.input_address.setSizePolicy(sizePolicy)
        self.input_address.setMaxLength(21)
        self.input_address.setObjectName("input_address")
        self.gridLayout.addWidget(self.input_address, 2, 0, 1, 2)
        self.input_password = QtWidgets.QLineEdit(parent=self.frame_menu)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_password.sizePolicy().hasHeightForWidth())
        self.input_password.setSizePolicy(sizePolicy)
        self.input_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.input_password.setObjectName("input_password")
        self.gridLayout.addWidget(self.input_password, 1, 0, 1, 2)
        self.input_username = QtWidgets.QLineEdit(parent=self.frame_menu)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_username.sizePolicy().hasHeightForWidth())
        self.input_username.setSizePolicy(sizePolicy)
        self.input_username.setObjectName("input_username")
        self.gridLayout.addWidget(self.input_username, 0, 0, 1, 2)
        self.horizontalLayout.addWidget(self.frame_menu)

        self.retranslateUi(Menu)
        QtCore.QMetaObject.connectSlotsByName(Menu)

    def retranslateUi(self, Menu):
        _translate = QtCore.QCoreApplication.translate
        Menu.setWindowTitle(_translate("Menu", "Form"))
        self.btn_host.setText(_translate("Menu", "Host server"))
        self.btn_connect.setText(_translate("Menu", "Connect"))
        self.input_address.setText(_translate("Menu", "127.0.0.1:54321"))
        self.input_address.setPlaceholderText(_translate("Menu", "Server address"))
        self.input_password.setPlaceholderText(_translate("Menu", "Password"))
        self.input_username.setPlaceholderText(_translate("Menu", "Username"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Menu = QtWidgets.QWidget()
    ui = Ui_Menu()
    ui.setupUi(Menu)
    Menu.show()
    sys.exit(app.exec())
