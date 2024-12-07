from __future__ import annotations

import sys
from warnings import filterwarnings
from threading import Thread
from queue import SimpleQueue
from toolkit.networking import ClientServer

import gui
from PyQt6.QtCore import pyqtSignal, pyqtSlot, QObject, QTimer
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QDialog, QMenu
)


filterwarnings(action="ignore", message="sipPyTypeDict()", category=DeprecationWarning)

STYLESHEET = open("gui/styles.css", "r").read()


def parse_address(address: str):
    address_split = address.split(":")
    if len(address_split) != 2 or not address_split[1].isdigit(): return

    port = int(address_split[1])
    if port < 49152 or port > 65535: return

    address = address_split[0]
    address_split = address.split(".")
    if len(address_split) != 4: return
    for part in address_split:
        if not part.isdigit(): return
        part = int(part)
        if part < 0 or part > 255: return

    return address, port


class Server(QWidget):  # TODO
    def handle_connection(self, socket, client, addr):
        pass


class KickDialog(QDialog, gui.Ui_KickDialog):
    def __init__(self, reason: str):
        super().__init__()
        self.setupUi(self)
        self.label_reason.setText(f"Reason:{reason}")
        self.show()


class PlayerListItem(QWidget, gui.Ui_PlayerListItem):
    def __init__(self, room: Room, name: str):
        super().__init__()
        self.setupUi(self)
        self.room = room
        self.name = name
        self.is_you = self.name == self.room.main.room_browser.username
        self.ready = False
        self.has_host_actions = False

        if self.room.host == self.room.main.room_browser.username:
            self.add_host_actions()

        self.icon_host.setMaximumWidth(16 if self.room.host == name else 0)
        self.label_username.setText(self.name + " (you)" if self.is_you else self.name)

        self.room.layout_players.addWidget(self)

    def set_ready(self, ready: bool):
        if self.ready and not ready: self.room.ready_players -= 1
        elif not self.ready and ready: self.room.ready_players += 1
        self.ready = ready
        self.setProperty("selected", ready)
        self.setStyleSheet(STYLESHEET)

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

    def __del__(self):
        self.room.layout_players.removeWidget(self)
        if self.ready:
            self.room.ready_players -= 1


class Room(QWidget, gui.Ui_Room):
    def __init__(self, main: Window, name: str, max_players: int, player_list: list[str], host: str):
        super().__init__()
        self.setupUi(self)
        self.main = main

        self.max_players = max_players
        self.players = {}
        self.ready_players = 0
        self.current_player: PlayerListItem | None = None
        self.used_words = []
        self.host = host

        self.countdown = 3
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.turn_time = 0
        self.turn_timer = QTimer()
        self.turn_timer.timeout.connect(self.update_turn_timer)

        self.label_room_name.setText(name)
        for player_name in player_list:
            self.players[player_name] = PlayerListItem(self, player_name)
        self.label_player_count.setText(f"{len(self.players)}/{self.max_players}")

        self.btn_leave.clicked.connect(self.leave_room)
        self.btn_ready.clicked.connect(self.ready_clicked)
        self.btn_submit.clicked.connect(self.submit_word)
        self.input_word.returnPressed.connect(self.submit_word)

        self.main.comm.recv_signal.connect(self.on_recv_message)

    @pyqtSlot()
    def update_countdown(self):
        self.countdown_timer.stop()
        self.label_game_state.setText(f"Starting in {self.countdown}...")
        self.countdown -= 1
        if self.countdown > 0:
            self.countdown_timer.start(1000)

    @pyqtSlot()
    def update_turn_timer(self):
        self.timer_progress.setValue(self.turn_time)
        if self.turn_time > 0:
            self.turn_time -= 1
        else:
            self.turn_timer.stop()

    def set_host(self, host: str):
        self.host = host
        self.players[host].icon_host.setMaximumWidth(16)
        if host == self.main.room_browser.username:
            for player in self.players.values():
                player.add_host_actions()

    def update_list(self, updates: list):
        for upd in updates:
            if upd["action"] == "del":
                self.players.pop(upd["name"], __default=None)
                if self.current_player.name == upd["name"]:
                    self.current_player: PlayerListItem | None = None
            elif upd["action"] == "add":
                self.players[upd["name"]] = PlayerListItem(self, upd["name"])
            elif upd["action"] == "upd":
                if "ready" in upd:
                    self.players[upd["name"]].set_ready(upd["ready"])
                    if not upd["ready"]:
                        self.countdown_timer.stop()
                        self.label_game_state.setText("Waiting for players...")
                if "host" in upd:
                    self.set_host(upd["name"])
        self.label_player_count.setText(f"{len(self.players)}/{self.max_players}")

    @pyqtSlot(dict)
    def on_recv_message(self, msg: dict):
        if msg["type"] == "event":
            if msg["event"] == "turn":
                self.next_turn(msg["body"])
            elif msg["event"] == "player-list-upd":
                self.update_list(msg["body"])
            elif msg["event"] == "start-countdown":
                self.countdown = 3
                self.update_countdown()
            elif msg["event"] == "kick":
                self.main.leave_room()
                KickDialog(msg["body"])

    def next_turn(self, turn_info: dict):
        if "word" in turn_info:
            self.output_words.append(turn_info["word"])
            self.used_words.append(turn_info["word"].lower())
        self.btn_ready.setEnabled(False)
        self.turn_time = 3000
        self.turn_timer.start(10)
        your_turn = turn_info["player"] == self.main.room_browser.username
        if your_turn:
            self.label_game_state.setText("Your turn")
            self.btn_submit.setEnabled(True)
            self.input_word.setEnabled(True)
            self.input_word.setFocus()
        else:
            self.label_game_state.setText(f"{turn_info['player']}'s turn")
        if self.current_player is not None: self.current_player.set_ready(False)
        self.current_player = self.players[turn_info["player"]]
        self.current_player.set_ready(True)

    @pyqtSlot()
    def submit_word(self):
        word = self.input_word.text().strip()
        if len(word) == 0: return
        self.input_word.clear()
        word_lower = word.lower()
        if self.used_words and not word_lower.startswith(self.used_words[-1][-1]):
            self.input_word.setPlaceholderText("Word's first letter must match last word's last letter")
        elif word_lower in self.used_words:
            self.input_word.setPlaceholderText("This word has already been used")
        else:
            self.input_word.setPlaceholderText("Type your word here...")
            self.used_words.append(word_lower)
            self.main.comm.send_queue.put({
                "type": "word",
                "word": word
            })
            self.input_word.setEnabled(False)
            self.btn_submit.setEnabled(False)

    @pyqtSlot(bool)
    def ready_clicked(self, toggled: bool):
        self.main.comm.send_queue.put({
            "type": "event",
            "event": "ready",
            "body": toggled
        })

    def leave_room(self):
        self.main.comm.send_queue.put({
            "type": "event",
            "event": "leave-room"
        })
        self.main.leave_room()

    def __del__(self):
        self.main.comm.recv_signal.disconnect(self.on_recv_message)


class RoomListItem(QWidget, gui.Ui_RoomListItem):
    def __init__(self, browser: RoomBrowser, name: str, player_count: int, max_players: int):
        super().__init__()
        self.setupUi(self)
        self.browser = browser
        self.name = name
        self.player_count = player_count
        self.max_players = max_players

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
        self.setStyleSheet(STYLESHEET)

    def deselect(self):
        self.browser.btn_join.setEnabled(False)
        self.setProperty("selected", False)
        self.setStyleSheet(STYLESHEET)

    def update_player_count(self, player_count: int):
        self.player_count = player_count
        self.label_playercount.setText(f"{self.player_count}/{self.max_players}")

    def __del__(self):
        if self.browser.selected_room == self:
            self.deselect()
        self.browser.layout_roomlist.removeWidget(self)


class RoomBrowser(QWidget, gui.Ui_RoomBrowser):
    def __init__(self, main: Window, username: str):
        super().__init__()
        self.setupUi(self)
        self.main = main
        self.username = username
        self.rooms = {}
        self.selected_room: RoomListItem | None = None

        self.btn_disconnect.clicked.connect(self.disconnect_from_server)
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
                self.rooms.pop(upd["name"], __default=None)
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

    @pyqtSlot()
    def disconnect_from_server(self):
        Thread(target=self.main.comm.socket.disconnect, daemon=True).start()
        self.main.exit_to_menu()

    def __del__(self):
        self.main.comm.recv_signal.disconnect(self.on_recv_message)


class Menu(QWidget, gui.Ui_Menu):
    def __init__(self, main: Window):
        super().__init__(main)
        self.setupUi(self)
        self.main = main

        self.btn_connect.clicked.connect(self.connect_clicked)
        self.btn_host.clicked.connect(self.host_clicked)

        self.main.comm.host_signal.connect(self.host_finished)
        self.main.comm.connect_signal.connect(self.connect_finished)

    @pyqtSlot()
    def host_clicked(self):
        addr = parse_address(self.input_address.text())
        self.input_password.setProperty("highlight-incorrect", False)
        self.input_address.setProperty("highlight-incorrect", addr is None)
        self.input_address.setStyleSheet(STYLESHEET)
        if addr is None: return
        self.setEnabled(False)
        self.btn_host.setText("Hosting...")
        self.main.server = Server(self.main)
        Thread(target=self.main.comm.host_server, args=(self.main.server.handle_connection, addr), daemon=True).start()

    @pyqtSlot(bool)
    def host_finished(self, success: bool):
        self.setEnabled(True)
        self.btn_host.setText("Host server")
        self.input_address.setProperty("highlight-incorrect", not success)
        self.setStyleSheet(STYLESHEET)

    @pyqtSlot()
    def connect_clicked(self):
        addr = parse_address(self.input_address.text())
        self.input_password.setProperty("highlight-incorrect", False)
        self.input_address.setProperty("highlight-incorrect", addr is None)
        self.setStyleSheet(STYLESHEET)
        if addr is None: return
        self.btn_connect.setText("Connecting...")
        self.setEnabled(False)
        Thread(target=self.main.comm.connect_to_server, args=(
            addr,
            self.input_username.text(),
            self.input_password.text()
        ), daemon=True).start()

    @pyqtSlot(dict)
    def connect_finished(self, result: dict):
        self.setEnabled(True)
        self.btn_connect.setText("Connect")
        self.input_password.setProperty("highlight-incorrect", result["body"] == "auth failed")
        self.input_address.setProperty("highlight-incorrect", result["event"] == "disconnect")
        self.setStyleSheet(STYLESHEET)


class Communication(QObject):
    connect_signal = pyqtSignal(dict)
    host_signal = pyqtSignal(bool)
    recv_signal = pyqtSignal(dict)
    send_queue = SimpleQueue()
    socket = ClientServer()

    def __init__(self):
        super().__init__()
        Thread(target=self.send_messages, daemon=True).start()

    def connect_to_server(self, addr, username, password):
        try:
            self.socket.connect(*addr)
            self.socket.send({
                "type": "event",
                "event": "connect",
                "username": username,
                "password": password
            })
            self.connect_signal.emit(self.socket.recv())
            Thread(target=self.recv_messages, daemon=True).start()
        except:
            self.connect_signal.emit({
                "type": "event",
                "event": "disconnect",
                "body": "connection lost"
            })

    def host_server(self, client_handling_func, addr):
        try:
            self.socket.host(client_handling_func, *addr)
            self.host_signal.emit(True)
        except:
            self.host_signal.emit(False)

    def send_messages(self):
        while True:
            data = self.send_queue.get()
            try:
                if data is tuple:
                    self.socket.send(*data)
                else:
                    self.socket.send(data)
            except: pass

    def recv_messages(self, recipient=None, recipient_name=""):
        while self.socket.is_open():
            data = self.socket.recv(recipient)
            data["from"] = recipient_name
            self.recv_signal.emit(data)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.comm = Communication()
        self.menu = Menu(self)
        self.room_browser: RoomBrowser | None = None
        self.room: Room | None = None
        self.server: Server | None = None

        self.comm.connect_signal.connect(self.connect_finished)
        self.comm.host_signal.connect(self.host_finished)

        self.setWindowTitle("WordGame")
        self.setCentralWidget(self.menu)

    @pyqtSlot(dict)
    def connect_finished(self, result: dict):
        if result["event"] != "connect" or result["body"] != "success": return
        self.room_browser = RoomBrowser(self, result["username"])
        self.setCentralWidget(self.room_browser)

    @pyqtSlot(bool)
    def host_finished(self, success: bool):
        if success:
            self.setCentralWidget(self.server)
        else:
            self.server = None

    def join_room(self, name: str, max_players: int, player_list: list[str], host: str):
        self.room = Room(self, name, max_players, player_list, host)
        self.setCentralWidget(self.room)

    def leave_room(self):
        self.room_browser.refresh()
        self.setCentralWidget(self.room_browser)
        self.room = None

    def exit_to_menu(self):
        self.setCentralWidget(self.menu)
        self.room = None
        self.room_browser = None
        self.server = None


app = QApplication(sys.argv)
app.setStyleSheet(STYLESHEET)
window = Window()
window.show()
app.exec()
