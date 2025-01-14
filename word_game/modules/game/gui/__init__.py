from .recompile import recompile_ui

from PyQt6.QtCore import QDir
QDir.addSearchPath("res", "modules/gui")

from .game import Ui_Game
