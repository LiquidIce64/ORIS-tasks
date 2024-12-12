import sys
from warnings import filterwarnings

from PyQt6.QtWidgets import QApplication

from modules import Window, Resources

filterwarnings(action="ignore", message="sipPyTypeDict()", category=DeprecationWarning)

app = QApplication(sys.argv)
STYLESHEET = open("modules/gui/styles.css", "r").read()
RESOURCES = Resources()
app.setStyleSheet(STYLESHEET)
window = Window(STYLESHEET, RESOURCES)
window.show()
app.exec()
