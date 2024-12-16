from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt, QTimer, pyqtSlot
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPixmap

from .player_list_item import ServerPlayerListItem
from .gui import Ui_RoomListItem, Ui_ServerRoomListItem, STYLESHEET
from .game import Game

if TYPE_CHECKING:
    from .room_browser import RoomBrowser
    from .server import Server


class RoomListItem(QWidget, Ui_RoomListItem):
    def __init__(self, browser: "RoomBrowser", name: str, player_count: int, max_players: int):
        super().__init__()
        self.setupUi(self)
        self.browser = browser
        self.name = name
        self.player_count = player_count
        self.max_players = max_players

        self.setStyleSheet(STYLESHEET)
        self.setAttribute(Qt.WidgetAttribute.WA_StyleSheet)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        self.label_name.setText(name)
        self.label_playercount.setText(f"{self.player_count}/{self.max_players}")

        self.browser.layout_roomlist.addWidget(self)

    def mousePressEvent(self, event):
        self.select()

    def mouseDoubleClickEvent(self, event):
        self.select()
        self.browser.join_room()

    def select(self):
        if self.browser.selected_room == self: return
        if self.browser.selected_room is not None:
            self.browser.selected_room.deselect()
        self.browser.selected_room = self
        self.browser.btn_join.setEnabled(True)
        self.browser.btn_join.setText("Join room")
        self.setProperty("selected", True)
        self.setStyleSheet(STYLESHEET)

    def deselect(self):
        self.browser.selected_room = None
        self.browser.btn_join.setEnabled(False)
        self.setProperty("selected", False)
        self.setStyleSheet(STYLESHEET)

    def update_player_count(self, player_count: int):
        self.player_count = player_count
        self.label_playercount.setText(f"{self.player_count}/{self.max_players}")

    def deleteLater(self):
        if self.browser.selected_room == self:
            self.deselect()
        super().deleteLater()


class ServerRoomListItem(QWidget, Ui_ServerRoomListItem):
    def __init__(self, server: "Server", name: str, max_players: int, host_item: ServerPlayerListItem):
        super().__init__()
        self.setupUi(self)
        self.server = server
        self.name = name
        self.players: dict[str, ServerPlayerListItem] = {host_item.name: host_item}
        self.max_players = max_players
        self.ready_players = 0
        self.game: Game | None = None
        host_item.set_host(True)

        self.server.room_list_upd.append({
            "action": "add",
            "name": self.name,
            "players": 1,
            "max": self.max_players
        })

        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.start_game)

        self.setStyleSheet(STYLESHEET)
        self.setAttribute(Qt.WidgetAttribute.WA_StyleSheet)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        self.label_name.setText(name)
        self.label_playercount.setText(f"{len(self.players)}/{self.max_players}")

        self.arrow_up = QPixmap("res:/icons/arrow_up.png")
        self.arrow_down = QPixmap("res:/icons/arrow_down.png")
        self.icon_arrow.setPixmap(self.arrow_up)
        self.frame_player_list.setMaximumHeight(0)

        self.icon_arrow.mousePressEvent =\
            self.label_name.mousePressEvent =\
            self.label_playercount.mousePressEvent = lambda *_: self.collapse()

        self.layout_player_list.addWidget(host_item)
        self.server.layout_roomlist.addWidget(self)

    def collapse(self):
        if self.frame_player_list.maximumHeight() == 0:
            self.frame_player_list.setMaximumHeight(16777215)
            self.icon_arrow.setPixmap(self.arrow_down)
        else:
            self.frame_player_list.setMaximumHeight(0)
            self.icon_arrow.setPixmap(self.arrow_up)

    @pyqtSlot()
    def start_game(self):
        self.countdown_timer.stop()
        for player in self.players.values():
            player.ready = False
        self.ready_players = 0
        self.game = Game(self)

    def check_ready(self):
        if self.ready_players == len(self.players):
            self.broadcast({
                "type": "event",
                "event": "start-countdown"
            })
            self.countdown_timer.start(3000)
        else:
            self.countdown_timer.stop()

    def set_ready(self, username: str, ready: bool):
        prev_ready = self.players[username].ready
        if prev_ready == ready: return
        if prev_ready and not ready:
            self.ready_players -= 1
        else:
            self.ready_players += 1
        self.players[username].ready = ready
        self.broadcast({
            "type": "event",
            "event": "player-list-upd",
            "body": [{
                "action": "upd",
                "name": username,
                "ready": ready
            }]
        })
        self.check_ready()

    def broadcast(self, msg: dict):
        for player in self.players.values():
            self.server.main.comm.send_queue.put((msg, self.server.clients[player.name]))

    def add_player(self, player_item: ServerPlayerListItem):
        self.broadcast({
            "type": "event",
            "event": "player-list-upd",
            "body": [{
                "action": "add",
                "name": player_item.name
            }]
        })
        self.players[player_item.name] = player_item
        self.layout_player_list.addWidget(player_item)
        self.label_playercount.setText(f"{len(self.players)}/{self.max_players}")
        self.server.room_list_upd.append({
            "action": "upd",
            "name": self.name,
            "players": len(self.players)
        })
        self.countdown_timer.stop()

    def remove_player(self, username: str, room_deleting=False):
        updates = [{
            "action": "del",
            "name": username
        }]
        player_item = self.players.pop(username)
        self.layout_player_list.removeWidget(player_item)
        if player_item.ready:
            player_item.ready = False
            self.ready_players -= 1

        if room_deleting: return player_item

        if player_item.host:
            player_item.set_host(False)
            if len(self.players) > 0:
                new_host = list(self.players.values())[0]
                new_host.set_host(True)
                updates.append({
                    "action": "upd",
                    "name": new_host.name,
                    "host": True
                })
        if len(self.players) == 0: self.deleteLater()

        self.label_playercount.setText(f"{len(self.players)}/{self.max_players}")
        self.server.room_list_upd.append({
            "action": "upd",
            "name": self.name,
            "players": len(self.players)
        })
        self.broadcast({
            "type": "event",
            "event": "player-list-upd",
            "body": updates
        })
        self.check_ready()

        if self.game is not None:
            self.game.remove_player(username)

        return player_item

    def deleteLater(self):
        self.countdown_timer.stop()
        if self.game is not None: self.game.deleteLater()
        self.broadcast({
            "type": "event",
            "event": "kick",
            "body": "Room closed"
        })
        for username, player_item in self.players.items():
            self.server.room_clients.pop(username)
            self.layout_player_list.removeWidget(player_item)
            player_item.ready = False
            self.server.browser_clients[username] = player_item
            self.server.layout_playerlist.addWidget(player_item)
        self.players.clear()
        self.server.label_players_in_rooms.setText(str(len(self.server.room_clients)))
        self.server.rooms.pop(self.name)
        self.server.room_list_upd.append({
            "action": "del",
            "name": self.name
        })
        super().deleteLater()
