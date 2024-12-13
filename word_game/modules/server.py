from typing import TYPE_CHECKING

from passlib.hash import pbkdf2_sha256 as sha256
from threading import Thread
from socket import socket as socket_raw
import json
from .networking import ClientServer

from PyQt6.QtCore import pyqtSlot, pyqtSignal, QTimer
from PyQt6.QtWidgets import QWidget

from .player_list_item import ServerPlayerListItem
from .room_list_item import ServerRoomListItem
from .gui import Ui_Server

if TYPE_CHECKING:
    from .window import Window


class Server(QWidget, Ui_Server):
    client_connect_signal = pyqtSignal(str)

    def __init__(self, main: "Window"):
        super().__init__()
        self.setupUi(self)
        self.main = main
        self.setStyleSheet(self.main.stylesheet)

        self.clients: dict[str, socket_raw] = {}
        self.browser_clients: dict[str, ServerPlayerListItem] = {}
        self.room_clients: dict[str, ServerRoomListItem] = {}
        self.rooms = {}
        self.room_list_full = {
            "type": "event",
            "event": "room-list-upd",
            "body": {
                "reset": True,
                "updates": []
            }
        }
        self.room_list_upd = []

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.send_room_list_upd)

        self.next_guest_id = 1
        try:
            self.passwords: dict = json.load(open("passwords.json", "r"))
        except:
            self.passwords = {}

        self.btn_stop.clicked.connect(self.main.exit_to_menu)

        self.client_connect_signal.connect(self.add_client)
        self.main.comm.recv_signal.connect(self.on_recv_message)

    def handle_connection(self, socket: ClientServer, client: socket_raw, addr):
        print(addr)
        connect_msg = socket.recv()
        print(connect_msg)
        if (
            connect_msg["type"] != "event" or
            connect_msg["event"] != "connect" or
            "username" not in connect_msg or
            "password" not in connect_msg
        ):
            print(addr, "cancelled")
            client.close()
            return

        username = str(connect_msg["username"]).strip()
        if len(username) == 0 or username.lower().startswith("guest"):
            username = f"Guest_{self.next_guest_id}"
            self.next_guest_id += 1
        else:
            password = str(connect_msg["password"])
            if username in self.passwords:
                if not sha256.verify(password, self.passwords[username]):
                    socket.send({
                        "type": "event",
                        "event": "connect",
                        "body": "auth failed"
                    }, client)
                    client.close()
                    return
            else:
                self.passwords[username] = sha256.hash(password)

        socket.send({
            "type": "event",
            "event": "connect",
            "body": "success",
            "username": username
        }, client)
        self.clients[username] = client
        self.client_connect_signal.emit(username)
        Thread(target=self.main.comm.recv_messages(client, username))

    @pyqtSlot(str)
    def add_client(self, username: str):
        self.browser_clients[username] = ServerPlayerListItem(self, username)
        self.label_player_count.setText(str(len(self.clients)))

    def remove_client(self, username: str):
        if username in self.browser_clients:
            self.browser_clients.pop(username).deleteLater()
        elif username in self.room_clients:
            room = self.room_clients.pop(username)
            room.players.pop(username).deleteLater()
            self.label_players_in_rooms.setText(str(len(self.room_clients)))
        if username in self.clients: self.clients.pop(username)
        self.label_player_count.setText(str(len(self.clients)))

    @pyqtSlot(dict)
    def on_recv_message(self, msg: dict):
        if msg["type"] == "event":
            if msg["event"] == "room-list-upd":
                self.send_room_list(msg["from"])
            elif msg["event"] == "join-room":
                pass
            elif msg["event"] == "create-room":
                pass
            elif msg["event"] == "disconnect":
                self.remove_client(msg["from"])

    def send_room_list(self, username: str):
        self.main.comm.send_queue.put(
            (self.room_list_full, self.clients[username])
        )

    def send_room_list_upd(self):
        if len(self.browser_clients) > 0:
            upd = {
                "type": "event",
                "event": "room-list-upd",
                "body": {
                    "reset": False,
                    "updates": self.room_list_upd
                }
            }
            for client in self.browser_clients.values():
                self.main.comm.send_queue.put(
                    (upd, self.clients[client.name])
                )

        self.room_list_upd = []
        self.room_list_full = {
            "type": "event",
            "event": "room-list-upd",
            "body": {
                "reset": True,
                "updates": [{
                    "action": "add",
                    "name": room.name,
                    "players": len(room.players),
                    "max": room.max_players
                } for room in self.rooms.values()]
            }
        }

    def deleteLater(self):
        json.dump(self.passwords, open("passwords.json", "w"))
        self.main.server = None
        super().deleteLater()
