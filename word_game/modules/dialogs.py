from PyQt6.QtWidgets import QDialog

from .gui import Ui_KickDialog


class KickDialog(QDialog, Ui_KickDialog):
    def __init__(self, reason: str):
        super().__init__()
        self.setupUi(self)
        self.label_reason.setText(f"Reason: {reason}")


class DisconnectDialog(KickDialog):
    def __init__(self, reason: str):
        super().__init__(reason)
        self.label_message.setText("Disconnected from server")
