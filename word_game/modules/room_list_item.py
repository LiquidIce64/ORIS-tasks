from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget

from .gui import Ui_RoomListItem, Ui_ServerRoomListItem
from .player_list_item import ServerPlayerListItem

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

        self.setStyleSheet(self.browser.main.stylesheet)
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
        self.browser.btn_join.setEnabled(True)
        self.browser.btn_join.setText("Join room")
        self.setProperty("selected", True)
        self.setStyleSheet(self.browser.main.stylesheet)

    def deselect(self):
        self.browser.btn_join.setEnabled(False)
        self.setProperty("selected", False)
        self.setStyleSheet(self.browser.main.stylesheet)

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
        host_item.set_host(True)

        self.server.room_list_upd.append({
            "action": "add",
            "name": self.name,
            "players": 1,
            "max": self.max_players
        })

        self.setStyleSheet(self.server.main.stylesheet)
        self.setAttribute(Qt.WidgetAttribute.WA_StyleSheet)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        self.label_name.setText(name)
        self.label_playercount.setText(f"{len(self.players)}/{self.max_players}")

        self.server.layout_roomlist.addWidget(self)

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

    def remove_player(self, username: str, room_deleting=False):
        updates = [{
            "action": "del",
            "name": username
        }]
        player_item = self.players.pop(username)
        self.layout_player_list.removeWidget(player_item)
        player_item.ready = False

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
        if len(self.players) > 0: self.deleteLater()

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
        return player_item

    def deleteLater(self):
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
