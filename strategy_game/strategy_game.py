import sys
from warnings import filterwarnings

from PyQt6.QtWidgets import QApplication

from modules import Window

filterwarnings(action="ignore", message="sipPyTypeDict()", category=DeprecationWarning)

app = QApplication(sys.argv)
window = Window()
window.show()
app.exec()
