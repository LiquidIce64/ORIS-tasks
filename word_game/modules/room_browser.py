from __future__ import annotations

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QWidget

from .room_list_item import RoomListItem
from .gui import Ui_RoomBrowser


class RoomBrowser(QWidget, Ui_RoomBrowser):
    def __init__(self, main, username: str):
        super().__init__()
        self.setupUi(self)
        self.main = main
        self.setStyleSheet(self.main.stylesheet)
        self.username = username
        self.rooms = {}
        self.selected_room: RoomListItem | None = None

        self.btn_disconnect.clicked.connect(self.main.exit_to_menu)
        self.btn_join.clicked.connect(self.join_room)
        self.btn_create.clicked.connect(self.create_room)

        self.main.comm.recv_signal.connect(self.on_recv_message)

    def refresh(self):
        self.main.comm.send_queue.put({
            "type": "event",
            "event": "room-list-upd"
        })

    def update_list(self, update_info: dict):
        if update_info["reset"]:
            self.rooms.clear()
        for upd in update_info["updates"]:
            if upd["action"] == "del":
                if upd["name"] in self.rooms: self.rooms.pop(upd["name"])
            elif upd["action"] == "add":
                self.rooms[upd["name"]] = RoomListItem(self, upd["name"], upd["players"], upd["max"])
            elif upd["action"] == "upd":
                self.rooms[upd["name"]].update_player_count(upd["players"])

    @pyqtSlot(dict)
    def on_recv_message(self, msg: dict):
        if msg["type"] == "event":
            if msg["event"] == "room-list-upd":
                self.update_list(msg["body"])

            elif msg["event"] == "join-room":
                self.setEnabled(True)
                if msg["body"] == "room joined":
                    self.btn_join.setText("Join room")
                    self.main.join_room(
                        name=self.selected_room.name,
                        max_players=self.selected_room.max_players,
                        player_list=msg["players"],
                        host=msg["host"]
                    )
                else:
                    self.btn_join.setText(msg["body"])

            elif msg["event"] == "create-room":
                self.setEnabled(True)
                if msg["body"] == "room created":
                    self.btn_create.setText("Create room")
                    self.main.join_room(
                        name=self.input_roomname.text(),
                        max_players=self.input_playercount.value(),
                        player_list=[self.username],
                        host=msg["host"]
                    )
                else:
                    self.btn_create.setText(msg["body"])

            elif msg["event"] == "disconnect":
                self.main.exit_to_menu()

    @pyqtSlot()
    def join_room(self):
        if self.selected_room is None: return
        self.setEnabled(False)
        self.btn_join.setText("Joining...")
        self.main.comm.send_queue.put({
            "type": "event",
            "event": "join-room",
            "name": self.selected_room.name
        })

    @pyqtSlot()
    def create_room(self):
        if len(self.input_roomname.text().strip()) == 0: return
        self.setEnabled(False)
        self.btn_create.setText("Creating...")
        self.main.comm.send_queue.put({
            "type": "event",
            "event": "create-room",
            "name": self.input_roomname.text(),
            "max-players": self.input_playercount.value()
        })
