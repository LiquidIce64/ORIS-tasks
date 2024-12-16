from .recompile import recompile_ui

from PyQt6.QtCore import QDir
QDir.addSearchPath("res", "modules/gui")

STYLESHEET = open("modules/gui/styles.css", "r").read()

from .menu import Ui_Menu
from .room_browser import Ui_RoomBrowser
from .room_list_item import Ui_RoomListItem
from .server_room_list_item import Ui_ServerRoomListItem
from .room import Ui_Room
from .player_list_item import Ui_PlayerListItem
from .kick_dialog import Ui_KickDialog
from .server import Ui_Server
