from __future__ import annotations
from typing import TYPE_CHECKING

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QWidget

from .dialogs import DisconnectDialog
from .room_list_item import RoomListItem
from .gui import Ui_RoomBrowser

if TYPE_CHECKING:
    from .window import Window


class RoomBrowser(QWidget, Ui_RoomBrowser):
    def __init__(self, main: "Window", username: str):
        super().__init__()
        self.setupUi(self)
        self.main = main
        self.username = username
        self.rooms: dict[str, RoomListItem] = {}
        self.selected_room: RoomListItem | None = None

        self.btn_disconnect.clicked.connect(self.main.exit_to_menu)
        self.btn_join.clicked.connect(self.join_room)
        self.btn_create.clicked.connect(self.create_room)

        self.main.comm.recv_signal.connect(self.on_recv_message)

        self.refresh()

    def refresh(self):
        self.main.comm.send_queue.put({
            "type": "event",
            "event": "room-list-upd"
        })

    def update_list(self, update_info: dict):
        if update_info["reset"]:
            for room in self.rooms.values():
                room.deleteLater()
            self.rooms.clear()
        for upd in update_info["updates"]:
            if upd["action"] == "del":
                if upd["name"] in self.rooms: self.rooms.pop(upd["name"]).deleteLater()
            elif upd["action"] == "add":
                self.rooms[upd["name"]] = RoomListItem(self, upd["name"], upd["players"], upd["max"])
            elif upd["action"] == "upd":
                if upd["name"] in self.rooms: self.rooms[upd["name"]].update_player_count(upd["players"])

    @pyqtSlot(dict)
    def on_recv_message(self, msg: dict):
        if msg["type"] == "event":
            if msg["event"] == "room-list-upd":
                self.update_list(msg["body"])

            elif msg["event"] == "join-room":
                self.setEnabled(True)
                if isinstance(msg["body"], list):
                    self.btn_join.setText("Join room")
                    self.main.join_room(
                        name=self.selected_room.name,
                        max_players=self.selected_room.max_players,
                        player_list=msg["body"]
                    )
                elif isinstance(msg["body"], str):
                    self.btn_join.setText(msg["body"])
                else:
                    print(f"[WARN] Unexpected response received while joining room ({msg['body']})")

            elif msg["event"] == "create-room":
                self.setEnabled(True)
                if msg["body"] == "Room created":
                    self.btn_create.setText("Create room")
                    self.main.join_room(
                        name=self.input_roomname.text(),
                        max_players=self.input_playercount.value(),
                        player_list=[{"name": self.username, "ready": False, "host": True}]
                    )
                else:
                    self.btn_create.setText(msg["body"])

            elif msg["event"] == "disconnect":
                self.main.exit_to_menu()
                DisconnectDialog(msg["body"], self.main).exec()

    @pyqtSlot()
    def join_room(self):
        if self.selected_room is None: return
        self.setEnabled(False)
        self.btn_join.setText("Joining...")
        self.main.comm.send_queue.put({
            "type": "event",
            "event": "join-room",
            "body": self.selected_room.name
        })

    @pyqtSlot()
    def create_room(self):
        name = self.input_roomname.text().strip()
        if len(name) == 0: return
        self.setEnabled(False)
        self.btn_create.setText("Creating...")
        self.main.comm.send_queue.put({
            "type": "event",
            "event": "create-room",
            "body": {
                "name": name,
                "max-players": self.input_playercount.value()
            }
        })

    def deleteLater(self):
        self.main.room_browser = None
        super().deleteLater()
