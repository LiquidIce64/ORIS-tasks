# Form implementation generated from reading ui file 'C:\Users\gilya\Projects\PyCharm\ORIS-tasks\word_game\modules\gui\room_list_item.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_RoomListItem(object):
    def setupUi(self, RoomListItem):
        RoomListItem.setObjectName("RoomListItem")
        RoomListItem.resize(150, 28)
        RoomListItem.setMinimumSize(QtCore.QSize(0, 28))
        self.horizontalLayout = QtWidgets.QHBoxLayout(RoomListItem)
        self.horizontalLayout.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_name = QtWidgets.QLabel(parent=RoomListItem)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_name.sizePolicy().hasHeightForWidth())
        self.label_name.setSizePolicy(sizePolicy)
        self.label_name.setMinimumSize(QtCore.QSize(100, 16))
        self.label_name.setMaximumSize(QtCore.QSize(16777215, 16))
        self.label_name.setObjectName("label_name")
        self.horizontalLayout.addWidget(self.label_name)
        self.label_playercount = QtWidgets.QLabel(parent=RoomListItem)
        self.label_playercount.setMinimumSize(QtCore.QSize(30, 16))
        self.label_playercount.setMaximumSize(QtCore.QSize(30, 16))
        self.label_playercount.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_playercount.setObjectName("label_playercount")
        self.horizontalLayout.addWidget(self.label_playercount)

        self.retranslateUi(RoomListItem)
        QtCore.QMetaObject.connectSlotsByName(RoomListItem)

    def retranslateUi(self, RoomListItem):
        _translate = QtCore.QCoreApplication.translate
        RoomListItem.setWindowTitle(_translate("RoomListItem", "Form"))
        self.label_name.setText(_translate("RoomListItem", "TextLabel"))
        self.label_playercount.setText(_translate("RoomListItem", "8/64"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RoomListItem = QtWidgets.QWidget()
    ui = Ui_RoomListItem()
    ui.setupUi(RoomListItem)
    RoomListItem.show()
    sys.exit(app.exec())
