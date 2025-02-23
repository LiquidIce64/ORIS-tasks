# Form implementation generated from reading ui file 'C:\Users\gilya\Projects\PyCharm\ORIS-tasks\strategy_game\modules\gui\server_room_list_item.ui'
#
# Created by: PyQt6 UI code generator 6.8.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ServerRoomListItem(object):
    def setupUi(self, ServerRoomListItem):
        ServerRoomListItem.setObjectName("ServerRoomListItem")
        ServerRoomListItem.resize(300, 100)
        ServerRoomListItem.setStyleSheet("#ServerRoomListItem {\n"
"    background-color: white;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: black;\n"
"    background: transparent;\n"
"}\n"
"QFrame {background: transparent}")
        self.layout_room_list_item = QtWidgets.QGridLayout(ServerRoomListItem)
        self.layout_room_list_item.setContentsMargins(10, 10, 10, 10)
        self.layout_room_list_item.setSpacing(0)
        self.layout_room_list_item.setObjectName("layout_room_list_item")
        self.icon_arrow = QtWidgets.QLabel(parent=ServerRoomListItem)
        self.icon_arrow.setMinimumSize(QtCore.QSize(16, 16))
        self.icon_arrow.setMaximumSize(QtCore.QSize(16, 16))
        self.icon_arrow.setText("")
        self.icon_arrow.setPixmap(QtGui.QPixmap("res:/icons/arrow_down.png"))
        self.icon_arrow.setScaledContents(True)
        self.icon_arrow.setObjectName("icon_arrow")
        self.layout_room_list_item.addWidget(self.icon_arrow, 0, 2, 1, 1)
        self.label_name = QtWidgets.QLabel(parent=ServerRoomListItem)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_name.sizePolicy().hasHeightForWidth())
        self.label_name.setSizePolicy(sizePolicy)
        self.label_name.setMinimumSize(QtCore.QSize(100, 16))
        self.label_name.setMaximumSize(QtCore.QSize(16777215, 16))
        self.label_name.setObjectName("label_name")
        self.layout_room_list_item.addWidget(self.label_name, 0, 0, 1, 1)
        self.label_playercount = QtWidgets.QLabel(parent=ServerRoomListItem)
        self.label_playercount.setMinimumSize(QtCore.QSize(30, 16))
        self.label_playercount.setMaximumSize(QtCore.QSize(30, 16))
        self.label_playercount.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_playercount.setObjectName("label_playercount")
        self.layout_room_list_item.addWidget(self.label_playercount, 0, 1, 1, 1)
        self.frame_player_list = QtWidgets.QFrame(parent=ServerRoomListItem)
        self.frame_player_list.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_player_list.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_player_list.setObjectName("frame_player_list")
        self.layout_player_list = QtWidgets.QVBoxLayout(self.frame_player_list)
        self.layout_player_list.setContentsMargins(3, 10, 3, 0)
        self.layout_player_list.setSpacing(3)
        self.layout_player_list.setObjectName("layout_player_list")
        self.layout_room_list_item.addWidget(self.frame_player_list, 1, 0, 1, 3)

        self.retranslateUi(ServerRoomListItem)
        QtCore.QMetaObject.connectSlotsByName(ServerRoomListItem)

    def retranslateUi(self, ServerRoomListItem):
        _translate = QtCore.QCoreApplication.translate
        ServerRoomListItem.setWindowTitle(_translate("ServerRoomListItem", "Form"))
        self.label_name.setText(_translate("ServerRoomListItem", "TextLabel"))
        self.label_playercount.setText(_translate("ServerRoomListItem", "8/64"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ServerRoomListItem = QtWidgets.QWidget()
    ui = Ui_ServerRoomListItem()
    ui.setupUi(ServerRoomListItem)
    ServerRoomListItem.show()
    sys.exit(app.exec())
