from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QWidget, QMenu

from .gui import Ui_PlayerListItem

if TYPE_CHECKING:
    from .room import Room
    from .server import Server


class PlayerListItem(QWidget, Ui_PlayerListItem):
    def __init__(self, room: "Room", name: str):
        super().__init__()
        self.setupUi(self)
        self.room = room
        self.setStyleSheet(self.room.main.stylesheet)
        self.name = name
        self.is_you = self.name == self.room.main.room_browser.username
        self.ready = False
        self.has_host_actions = False

        if self.room.host == self.room.main.room_browser.username:
            self.add_host_actions()

        self.icon_host.setPixmap(self.room.main.resources.host)
        self.icon_host.setMaximumWidth(16 if self.room.host == name else 0)
        self.label_username.setText(self.name + " (you)" if self.is_you else self.name)

        self.room.layout_players.addWidget(self)

    def set_ready(self, ready: bool):
        if self.ready and not ready: self.room.ready_players -= 1
        elif not self.ready and ready: self.room.ready_players += 1
        self.ready = ready
        self.setProperty("selected", ready)
        self.setStyleSheet(self.room.main.stylesheet)

    def add_host_actions(self):
        if self.has_host_actions or self.is_you: return
        self.has_host_actions = True
        context_menu = QMenu(self)
        kick_action = context_menu.addAction("Kick")
        kick_action.triggered.connect(self.kick)

    def kick(self):
        self.room.main.comm.send_queue.put({
            "type": "event",
            "event": "kick",
            "body": self.name
        })

    def deleteLater(self):
        if self.ready:
            self.room.ready_players -= 1
        super().deleteLater()


class ServerPlayerListItem(QWidget, Ui_PlayerListItem):
    def __init__(self, server: "Server", name: str, is_host=False):
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet(server.main.stylesheet)
        self.server = server
        self.name = name

        context_menu = QMenu(self)
        kick_action = context_menu.addAction("Kick")
        kick_action.triggered.connect(self.kick)

        self.icon_host.setPixmap(self.server.main.resources.host)
        self.icon_host.setMaximumWidth(16 if is_host else 0)
        self.label_username.setText(self.name)

        self.server.layout_playerlist.addWidget(self)

    def kick(self):
        self.server.main.comm.send_queue.put(
            ({
                "type": "event",
                "event": "kick",
                "body": "Kicked by server"
            }, self.server.clients[self.name])
        )
        self.server.remove_client(self.name)
