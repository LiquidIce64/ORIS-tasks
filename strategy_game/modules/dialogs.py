from PyQt6.QtWidgets import QDialog

from PyQt6.QtWidgets import QWidget
from .gui import Ui_KickDialog


class KickDialog(QDialog, Ui_KickDialog):
    def __init__(self, reason: str, parent: QWidget = None):
        super().__init__(parent)
        self.setupUi(self)
        self.label_reason.setText(f"Reason: {reason}")


class DisconnectDialog(KickDialog):
    def __init__(self, reason: str, parent: QWidget = None):
        super().__init__(reason, parent)
        self.label_message.setText("Disconnected from server")
