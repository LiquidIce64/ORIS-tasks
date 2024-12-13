import sys
from warnings import filterwarnings

from PyQt6.QtWidgets import QApplication

from modules import Window

filterwarnings(action="ignore", message="sipPyTypeDict()", category=DeprecationWarning)

app = QApplication(sys.argv)
STYLESHEET = open("modules/gui/styles.css", "r").read()
app.setStyleSheet(STYLESHEET)
window = Window(STYLESHEET)
window.show()
app.exec()
