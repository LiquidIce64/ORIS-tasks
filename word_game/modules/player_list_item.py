from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QMenu
from PyQt6.QtGui import QContextMenuEvent, QIcon

from .gui import Ui_PlayerListItem

if TYPE_CHECKING:
    from .room import Room
    from .server import Server


class PlayerListItem(QWidget, Ui_PlayerListItem):
    def __init__(self, room: "Room", name: str, ready=False):
        super().__init__()
        self.setupUi(self)
        self.room = room
        self.name = name
        self.is_you = self.name == self.room.main.room_browser.username
        self.ready = ready
        self.has_host_actions = False

        if self.room.host == self.room.main.room_browser.username:
            self.add_host_actions()

        self.context_menu = QMenu(self)
        self.context_menu.addAction(QIcon("res:/icons/kick.png"), "Kick from room").triggered.connect(self.kick)

        if ready: self.setProperty("selected", ready)

        self.icon_host.setMaximumWidth(16 if self.room.host == name else 0)
        self.label_username.setText(self.name + " (you)" if self.is_you else self.name)

        self.setAttribute(Qt.WidgetAttribute.WA_StyleSheet)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        self.room.layout_players.addWidget(self)

    def set_ready(self, ready: bool):
        if self.ready and not ready: self.room.ready_players -= 1
        elif not self.ready and ready: self.room.ready_players += 1
        self.ready = ready
        self.setProperty("selected", ready)
        self.setStyleSheet(self.styleSheet())

    def add_host_actions(self):
        if not self.is_you:
            self.has_host_actions = True

    def contextMenuEvent(self, event: QContextMenuEvent):
        if self.has_host_actions:
            self.context_menu.exec(event.globalPos())

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
    def __init__(self, server: "Server", name: str):
        super().__init__()
        self.setupUi(self)
        self.server = server
        self.name = name
        self.ready = False
        self.host = False

        self.context_menu = QMenu(self)
        self.context_menu.addAction(QIcon("res:/icons/kick.png"), "Kick from server").triggered.connect(self.kick)

        self.icon_host.setMaximumWidth(0)
        self.label_username.setText(self.name)

        self.setAttribute(Qt.WidgetAttribute.WA_StyleSheet)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        self.server.layout_playerlist.addWidget(self)

    def contextMenuEvent(self, event: QContextMenuEvent):
        self.context_menu.exec(event.globalPos())

    def set_host(self, host: bool):
        self.host = host
        self.icon_host.setMaximumWidth(16 if host else 0)

    def kick(self):
        client = self.server.clients[self.name]
        self.server.main.comm.send_queue.put(({
                "type": "event",
                "event": "disconnect",
                "body": "Kicked from server"
        }, client))
