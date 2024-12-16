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
        self.rooms: dict[str, ServerRoomListItem] = {}
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
        self.update_timer.start(5000)

        self.next_guest_id = 1
        try:
            self.passwords: dict = json.load(open("passwords.json", "r"))
        except:
            self.passwords = {}

        self.btn_stop.clicked.connect(self.main.exit_to_menu)

        self.client_connect_signal.connect(self.add_client)
        self.main.comm.recv_signal.connect(self.on_recv_message)

    def handle_connection(self, socket: ClientServer, client: socket_raw, addr):
        connect_msg = socket.recv(client)
        if (
            "type" not in connect_msg or
            connect_msg["type"] != "event" or
            "event" not in connect_msg or
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
        print(f"{username} connected from {addr}")
        Thread(target=self.main.comm.recv_messages(client, username), daemon=True).start()

    @pyqtSlot(str)
    def add_client(self, username: str):
        self.browser_clients[username] = ServerPlayerListItem(self, username)
        self.label_player_count.setText(str(len(self.clients)))

    def remove_client(self, username: str):
        if username in self.browser_clients:
            self.browser_clients.pop(username).deleteLater()
        elif username in self.room_clients:
            room = self.room_clients.pop(username)
            room.remove_player(username).deleteLater()
            self.label_players_in_rooms.setText(str(len(self.room_clients)))
        if username in self.clients: self.clients.pop(username)
        self.label_player_count.setText(str(len(self.clients)))

    @pyqtSlot(dict)
    def on_recv_message(self, msg: dict):
        try:
            if msg["type"] == "event":
                if msg["event"] == "room-list-upd":
                    self.main.comm.send_queue.put(
                        (self.room_list_full, self.clients[msg["from"]])
                    )

                elif msg["event"] == "join-room":
                    self.main.comm.send_queue.put(({
                        "type": "event",
                        "event": "join-room",
                        "body": self.join_room(msg["body"], msg["from"])
                    }, self.clients[msg["from"]]))

                elif msg["event"] == "leave-room":
                    self.leave_room(msg["from"])

                elif msg["event"] == "create-room":
                    self.main.comm.send_queue.put(({
                        "type": "event",
                        "event": "create-room",
                        "body": self.create_room(msg["body"], msg["from"])
                    }, self.clients[msg["from"]]))

                elif msg["event"] == "disconnect":
                    self.remove_client(msg["from"])

                elif msg["event"] == "kick":
                    self.kick_from_room(msg["body"], msg["from"])
        except KeyError:
            print(f"[WARN] Invalid keys in message, skipping...\nMessage: {msg}")

    @pyqtSlot()
    def send_room_list_upd(self):
        print("Sending room list update...")
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

    def join_room(self, room_name: str, username: str):
        if room_name not in self.rooms: return "Room not found"
        room = self.rooms[room_name]
        if len(room.players) >= room.max_players: return "Room full"
        if username not in self.browser_clients: return "Error"

        player_item = self.browser_clients.pop(username)
        self.layout_playerlist.removeWidget(player_item)
        room.add_player(player_item)
        self.room_clients[username] = room
        self.label_players_in_rooms.setText(str(len(self.room_clients)))

        return [{
            "name": player.name,
            "ready": player.ready,
            "host": player.host
        } for player in room.players.values()]

    def leave_room(self, username: str):
        if username not in self.room_clients: return
        room = self.room_clients.pop(username)
        player_item = room.remove_player(username)

        self.browser_clients[username] = player_item
        self.layout_playerlist.addWidget(player_item)
        self.label_players_in_rooms.setText(str(len(self.room_clients)))
        print(f"{username} left the room")

    def create_room(self, room_info: dict, host: str):
        if "name" not in room_info or "max-players" not in room_info: return "Error"
        name = room_info["name"]
        max_players = room_info["max-players"]
        if name in self.rooms: return "Room already exists"
        if not (2 <= max_players <= 64): return "Error"
        if host not in self.browser_clients: return "Error"

        host_item = self.browser_clients.pop(host)
        self.layout_playerlist.removeWidget(host_item)

        room = ServerRoomListItem(self, name, max_players, host_item)
        self.rooms[name] = room
        self.room_clients[host_item.name] = room
        self.label_players_in_rooms.setText(str(len(self.room_clients)))

        return "Room created"

    def kick_from_room(self, username, from_username):
        if from_username not in self.room_clients: return
        if username not in self.room_clients: return
        room = self.room_clients[from_username]
        if not room.players[from_username].host: return
        if username not in room.players: return
        self.leave_room(username)
        self.main.comm.send_queue.put(({
            "type": "event",
            "event": "kick",
            "body": "Kicked by host"
        }, self.clients[username]))
        print(f"{username} kicked from room")

    def deleteLater(self):
        json.dump(self.passwords, open("passwords.json", "w"))
        msg = {
            "type": "event",
            "event": "disconnect",
            "body": "Server closed"
        }
        for client in self.clients.values():
            self.main.comm.send_queue.put((msg, client))
        self.update_timer.stop()
        self.main.server = None
        super().deleteLater()
