# Form implementation generated from reading ui file 'C:\Users\gilya\Projects\PyCharm\ORIS-tasks\word_game\modules\gui\server.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Server(object):
    def setupUi(self, Server):
        Server.setObjectName("Server")
        Server.resize(500, 300)
        Server.setMinimumSize(QtCore.QSize(500, 300))
        self.horizontalLayout = QtWidgets.QHBoxLayout(Server)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_browser = QtWidgets.QFrame(parent=Server)
        self.frame_browser.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_browser.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_browser.setObjectName("frame_browser")
        self._2 = QtWidgets.QVBoxLayout(self.frame_browser)
        self._2.setObjectName("_2")
        self.scrollArea = QtWidgets.QScrollArea(parent=self.frame_browser)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 292, 278))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layout_roomlist = QtWidgets.QVBoxLayout()
        self.layout_roomlist.setSpacing(3)
        self.layout_roomlist.setObjectName("layout_roomlist")
        self.verticalLayout.addLayout(self.layout_roomlist)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self._2.addWidget(self.scrollArea)
        self.horizontalLayout.addWidget(self.frame_browser)
        self.line = QtWidgets.QFrame(parent=Server)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.frame_sidepanel = QtWidgets.QFrame(parent=Server)
        self.frame_sidepanel.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_sidepanel.setObjectName("frame_sidepanel")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_sidepanel)
        self.gridLayout.setContentsMargins(9, 9, 9, 9)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(parent=self.frame_sidepanel)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 2)
        self.label_player_count = QtWidgets.QLabel(parent=self.frame_sidepanel)
        self.label_player_count.setMinimumSize(QtCore.QSize(30, 16))
        self.label_player_count.setMaximumSize(QtCore.QSize(30, 16))
        self.label_player_count.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_player_count.setObjectName("label_player_count")
        self.gridLayout.addWidget(self.label_player_count, 6, 1, 1, 1)
        self.scrollArea_2 = QtWidgets.QScrollArea(parent=self.frame_sidepanel)
        self.scrollArea_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 129, 184))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.layout_playerlist = QtWidgets.QVBoxLayout()
        self.layout_playerlist.setSpacing(3)
        self.layout_playerlist.setObjectName("layout_playerlist")
        self.verticalLayout_3.addLayout(self.layout_playerlist)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_3)
        self.gridLayout.addWidget(self.scrollArea_2, 3, 0, 1, 2)
        self.btn_stop = QtWidgets.QPushButton(parent=self.frame_sidepanel)
        self.btn_stop.setObjectName("btn_stop")
        self.gridLayout.addWidget(self.btn_stop, 9, 0, 1, 2)
        self.label_players_in_rooms = QtWidgets.QLabel(parent=self.frame_sidepanel)
        self.label_players_in_rooms.setMinimumSize(QtCore.QSize(30, 16))
        self.label_players_in_rooms.setMaximumSize(QtCore.QSize(30, 16))
        self.label_players_in_rooms.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_players_in_rooms.setObjectName("label_players_in_rooms")
        self.gridLayout.addWidget(self.label_players_in_rooms, 7, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=self.frame_sidepanel)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 7, 0, 1, 1)
        self.label = QtWidgets.QLabel(parent=self.frame_sidepanel)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 6, 0, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.horizontalLayout.addWidget(self.frame_sidepanel)
        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(2, 1)

        self.retranslateUi(Server)
        QtCore.QMetaObject.connectSlotsByName(Server)

    def retranslateUi(self, Server):
        _translate = QtCore.QCoreApplication.translate
        Server.setWindowTitle(_translate("Server", "Form"))
        self.label_3.setText(_translate("Server", "Players browsing:"))
        self.label_player_count.setText(_translate("Server", "0"))
        self.btn_stop.setText(_translate("Server", "Stop Server"))
        self.label_players_in_rooms.setText(_translate("Server", "0"))
        self.label_2.setText(_translate("Server", "Players in rooms:"))
        self.label.setText(_translate("Server", "Players connected:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Server = QtWidgets.QWidget()
    ui = Ui_Server()
    ui.setupUi(Server)
    Server.show()
    sys.exit(app.exec())
