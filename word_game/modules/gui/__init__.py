from .recompile import recompile_ui

from PyQt6.QtCore import QDir
QDir.addSearchPath("res", "modules/gui")

from .menu import Ui_Menu
from .room_browser import Ui_RoomBrowser
from .room_list_item import Ui_RoomListItem
from .room import Ui_Room
from .player_list_item import Ui_PlayerListItem
from .kick_dialog import Ui_KickDialog
from .server import Ui_Server
