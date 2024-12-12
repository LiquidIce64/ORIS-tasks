from PyQt6.QtCore import QObject, QDir
from PyQt6.QtGui import QPixmap


class Resources(QObject):
    def __init__(self):
        super().__init__()
        QDir.addSearchPath("icons", "gui/icons")
        self.host = QPixmap("icons:host.png")
