from __future__ import annotations
from typing import TYPE_CHECKING

from PyQt6.QtCore import pyqtSlot, QTimer
from PyQt6.QtWidgets import QWidget

from .player_list_item import PlayerListItem
from .dialogs import KickDialog
from .gui import Ui_Room

if TYPE_CHECKING:
    from .window import Window


class Room(QWidget, Ui_Room):
    def __init__(self, main: "Window", name: str, max_players: int, player_list: list[str], host: str):
        super().__init__()
        self.setupUi(self)
        self.main = main
        self.setStyleSheet(self.main.stylesheet)

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
                if upd["name"] in self.players: self.players.pop(upd["name"])
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
                KickDialog(msg["body"]).exec()

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

    def deleteLater(self):
        self.main.room = None
        super().deleteLater()
