from PyQt6.QtCore import QDir
QDir.addSearchPath("shaders", "modules/game/shaders")
QDir.addSearchPath("textures", "modules/game/textures")

from .game import Game
from .game_server import GameServer
