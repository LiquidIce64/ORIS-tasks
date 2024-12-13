# Form implementation generated from reading ui file 'C:\Users\gilya\Projects\PyCharm\ORIS-tasks\word_game\modules\gui\room.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Room(object):
    def setupUi(self, Room):
        Room.setObjectName("Room")
        Room.resize(500, 300)
        Room.setMinimumSize(QtCore.QSize(500, 300))
        self.horizontalLayout = QtWidgets.QHBoxLayout(Room)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_game = QtWidgets.QFrame(parent=Room)
        self.frame_game.setObjectName("frame_game")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_game)
        self.gridLayout_2.setContentsMargins(9, 9, 9, 9)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.input_word = QtWidgets.QLineEdit(parent=self.frame_game)
        self.input_word.setEnabled(False)
        self.input_word.setObjectName("input_word")
        self.gridLayout_2.addWidget(self.input_word, 1, 0, 1, 1)
        self.btn_submit = QtWidgets.QPushButton(parent=self.frame_game)
        self.btn_submit.setEnabled(False)
        self.btn_submit.setObjectName("btn_submit")
        self.gridLayout_2.addWidget(self.btn_submit, 1, 1, 1, 1)
        self.output_words = QtWidgets.QTextEdit(parent=self.frame_game)
        self.output_words.setEnabled(True)
        self.output_words.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.output_words.setReadOnly(True)
        self.output_words.setObjectName("output_words")
        self.gridLayout_2.addWidget(self.output_words, 0, 0, 1, 2)
        self.horizontalLayout.addWidget(self.frame_game)
        self.line = QtWidgets.QFrame(parent=Room)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.frame_sidepanel = QtWidgets.QFrame(parent=Room)
        self.frame_sidepanel.setMinimumSize(QtCore.QSize(165, 0))
        self.frame_sidepanel.setObjectName("frame_sidepanel")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_sidepanel)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.gridLayout.setContentsMargins(9, 9, 9, 9)
        self.gridLayout.setObjectName("gridLayout")
        self.label_game_state = QtWidgets.QLabel(parent=self.frame_sidepanel)
        self.label_game_state.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_game_state.setObjectName("label_game_state")
        self.gridLayout.addWidget(self.label_game_state, 2, 0, 1, 3)
        self.label_room_name = QtWidgets.QLabel(parent=self.frame_sidepanel)
        self.label_room_name.setMinimumSize(QtCore.QSize(100, 16))
        self.label_room_name.setMaximumSize(QtCore.QSize(16777215, 16))
        self.label_room_name.setObjectName("label_room_name")
        self.gridLayout.addWidget(self.label_room_name, 0, 0, 1, 2)
        self.label_player_count = QtWidgets.QLabel(parent=self.frame_sidepanel)
        self.label_player_count.setMinimumSize(QtCore.QSize(30, 16))
        self.label_player_count.setMaximumSize(QtCore.QSize(30, 16))
        self.label_player_count.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_player_count.setObjectName("label_player_count")
        self.gridLayout.addWidget(self.label_player_count, 0, 2, 1, 1)
        self.btn_ready = QtWidgets.QPushButton(parent=self.frame_sidepanel)
        self.btn_ready.setMinimumSize(QtCore.QSize(0, 0))
        self.btn_ready.setCheckable(True)
        self.btn_ready.setObjectName("btn_ready")
        self.gridLayout.addWidget(self.btn_ready, 4, 0, 1, 1)
        self.btn_leave = QtWidgets.QPushButton(parent=self.frame_sidepanel)
        self.btn_leave.setMinimumSize(QtCore.QSize(64, 0))
        self.btn_leave.setMaximumSize(QtCore.QSize(64, 16777215))
        self.btn_leave.setObjectName("btn_leave")
        self.gridLayout.addWidget(self.btn_leave, 4, 1, 1, 2)
        self.scrollArea = QtWidgets.QScrollArea(parent=self.frame_sidepanel)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 129, 192))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.layout_players = QtWidgets.QVBoxLayout()
        self.layout_players.setSpacing(3)
        self.layout_players.setObjectName("layout_players")
        self.verticalLayout_2.addLayout(self.layout_players)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 1, 0, 1, 3)
        self.timer_progress = QtWidgets.QProgressBar(parent=self.frame_sidepanel)
        self.timer_progress.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timer_progress.sizePolicy().hasHeightForWidth())
        self.timer_progress.setSizePolicy(sizePolicy)
        self.timer_progress.setMaximumSize(QtCore.QSize(16777215, 8))
        self.timer_progress.setStyleSheet("")
        self.timer_progress.setMaximum(3000)
        self.timer_progress.setProperty("value", 0)
        self.timer_progress.setTextVisible(False)
        self.timer_progress.setObjectName("timer_progress")
        self.gridLayout.addWidget(self.timer_progress, 3, 0, 1, 3)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setRowStretch(1, 1)
        self.horizontalLayout.addWidget(self.frame_sidepanel)
        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(2, 1)

        self.retranslateUi(Room)
        QtCore.QMetaObject.connectSlotsByName(Room)
        Room.setTabOrder(self.input_word, self.btn_submit)
        Room.setTabOrder(self.btn_submit, self.btn_ready)
        Room.setTabOrder(self.btn_ready, self.btn_leave)
        Room.setTabOrder(self.btn_leave, self.scrollArea)
        Room.setTabOrder(self.scrollArea, self.output_words)

    def retranslateUi(self, Room):
        _translate = QtCore.QCoreApplication.translate
        Room.setWindowTitle(_translate("Room", "Form"))
        self.input_word.setPlaceholderText(_translate("Room", "Type your word here..."))
        self.btn_submit.setText(_translate("Room", "Submit"))
        self.label_game_state.setText(_translate("Room", "Waiting for players..."))
        self.label_room_name.setText(_translate("Room", "TextLabel"))
        self.label_player_count.setText(_translate("Room", "8/64"))
        self.btn_ready.setText(_translate("Room", "Not Ready"))
        self.btn_leave.setText(_translate("Room", "Leave"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Room = QtWidgets.QWidget()
    ui = Ui_Room()
    ui.setupUi(Room)
    Room.show()
    sys.exit(app.exec())
