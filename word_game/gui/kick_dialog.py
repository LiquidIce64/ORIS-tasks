# Form implementation generated from reading ui file 'C:\Users\gilya\Projects\PyCharm\ORIS-tasks\word_game\gui\kick_dialog.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_KickDialog(object):
    def setupUi(self, KickDialog):
        KickDialog.setObjectName("KickDialog")
        KickDialog.resize(175, 100)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(KickDialog.sizePolicy().hasHeightForWidth())
        KickDialog.setSizePolicy(sizePolicy)
        KickDialog.setMinimumSize(QtCore.QSize(175, 100))
        KickDialog.setMaximumSize(QtCore.QSize(175, 100))
        self.verticalLayout = QtWidgets.QVBoxLayout(KickDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_message = QtWidgets.QLabel(parent=KickDialog)
        self.label_message.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_message.setWordWrap(True)
        self.label_message.setObjectName("label_message")
        self.verticalLayout.addWidget(self.label_message)
        self.label_reason = QtWidgets.QLabel(parent=KickDialog)
        self.label_reason.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_reason.setObjectName("label_reason")
        self.verticalLayout.addWidget(self.label_reason)
        self.btn_ok = QtWidgets.QDialogButtonBox(parent=KickDialog)
        self.btn_ok.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.btn_ok.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.btn_ok.setCenterButtons(False)
        self.btn_ok.setObjectName("btn_ok")
        self.verticalLayout.addWidget(self.btn_ok)

        self.retranslateUi(KickDialog)
        self.btn_ok.accepted.connect(KickDialog.accept) # type: ignore
        self.btn_ok.rejected.connect(KickDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(KickDialog)

    def retranslateUi(self, KickDialog):
        _translate = QtCore.QCoreApplication.translate
        KickDialog.setWindowTitle(_translate("KickDialog", "WordGame"))
        self.label_message.setText(_translate("KickDialog", "Kicked from the room"))
        self.label_reason.setText(_translate("KickDialog", "Reason: Out of time"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    KickDialog = QtWidgets.QDialog()
    ui = Ui_KickDialog()
    ui.setupUi(KickDialog)
    KickDialog.show()
    sys.exit(app.exec())
