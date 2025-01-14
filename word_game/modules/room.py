from __future__ import annotations
from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt, pyqtSlot, QTimer
from PyQt6.QtWidgets import QWidget

from .player_list_item import PlayerListItem
from .dialogs import KickDialog
from .game import Game
from .gui import Ui_Room

if TYPE_CHECKING:
    from .window import Window


class Room(QWidget, Ui_Room):
    def __init__(self, main: "Window", name: str, max_players: int, player_list: list[dict]):
        super().__init__()
        self.setupUi(self)
        self.main = main

        self.max_players = max_players
        self.players: dict[str, PlayerListItem] = {}
        self.ready_players = 0
        self.current_player: PlayerListItem | None = None
        self.used_words = []

        self.countdown = 3
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.turn_time = 0
        self.turn_timer = QTimer()
        self.turn_timer.timeout.connect(self.update_turn_timer)
        self.game_started = False

        self.label_room_name.setText(name)
        for player_info in player_list:
            name = player_info["name"]
            if player_info["host"]: self.host = name
            self.players[name] = PlayerListItem(self, name, player_info["ready"])
        self.label_player_count.setText(f"{len(self.players)}/{self.max_players}")

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        self.btn_leave.clicked.connect(self.leave_room)
        self.btn_ready.clicked.connect(self.ready_clicked)

        self.main.comm.recv_signal.connect(self.on_recv_message)

        self.game = Game(self.main.comm)
        self.layout_game.addWidget(self.game)

    @pyqtSlot()
    def update_countdown(self):
        self.countdown_timer.stop()
        if self.game_started: return
        self.label_game_state.setText(f"Starting in {self.countdown}...")
        if self.countdown > 0:
            self.countdown -= 1
            self.countdown_timer.start(1000)

    @pyqtSlot()
    def update_turn_timer(self):
        self.timer_progress.setValue(self.turn_time)
        self.timer_progress.repaint()
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
                if upd["name"] in self.players:
                    self.players.pop(upd["name"]).deleteLater()
                if self.current_player is not None and self.current_player.name == upd["name"]:
                    self.current_player = None
                self.game.remove_team(upd["name"])
                self.countdown_timer.stop()
                if not self.game_started: self.label_game_state.setText("Waiting for players...")
            elif upd["action"] == "add":
                self.players[upd["name"]] = PlayerListItem(self, upd["name"])
                self.countdown_timer.stop()
                self.label_game_state.setText("Waiting for players...")
            elif upd["action"] == "upd":
                if "ready" in upd:
                    self.players[upd["name"]].set_ready(upd["ready"])
                    if not upd["ready"]:
                        self.countdown_timer.stop()
                        self.label_game_state.setText("Waiting for players...")
                if "host" in upd:
                    self.set_host(upd["name"])
        self.label_player_count.setText(f"{len(self.players)}/{self.max_players}")

    def start_game(self):
        self.game_started = True
        for i, player in enumerate(self.players.values()):
            player.set_ready(False)
            self.game.remaining_teams[player.name] = i
        self.btn_ready.setEnabled(False)
        self.btn_ready.setText("End turn")
        self.game.start_game()

    @pyqtSlot(dict)
    def on_recv_message(self, msg: dict):
        if msg["type"] == "event":
            if msg["event"] == "player-list-upd":
                self.update_list(msg["body"])

            elif msg["event"] == "start-countdown":
                self.countdown = 3
                self.update_countdown()

            elif msg["event"] == "kick":
                self.main.leave_room()
                KickDialog(msg["body"], self.main).exec()
        elif msg["type"] == "game-event":
            if msg["game-event"] == "move":
                self.game.make_move(msg["body"])

            elif msg["game-event"] == "turn":
                if not self.game_started: self.start_game()
                self.next_turn(msg["body"])

            elif msg["game-event"] == "create-unit":
                self.game.create_unit(msg["body"])

    def next_turn(self, next_player: str):
        self.turn_time = 12000
        self.turn_timer.start(10)
        if next_player == self.main.room_browser.username:
            self.label_game_state.setText("Your turn")
            self.btn_ready.setEnabled(True)
            self.game.next_turn(next_player)
        else:
            self.label_game_state.setText(f"{next_player}'s turn")
            self.btn_ready.setEnabled(False)
            self.game.next_turn(-1)
        if self.current_player is not None: self.current_player.set_ready(False)
        self.current_player = self.players[next_player]
        self.current_player.set_ready(True)

    @pyqtSlot(bool)
    def ready_clicked(self, toggled: bool):
        if self.game_started:
            self.btn_ready.setEnabled(False)
            self.main.comm.send_queue.put({
                "type": "game-event",
                "game-event": "turn"
            })
        else:
            self.btn_ready.setText("Ready" if toggled else "Not Ready")
            self.main.comm.send_queue.put({
                "type": "event",
                "event": "ready",
                "body": toggled
            })

    @pyqtSlot()
    def leave_room(self):
        self.main.comm.send_queue.put({
            "type": "event",
            "event": "leave-room"
        })
        self.main.leave_room()

    def deleteLater(self):
        self.main.room = None
        super().deleteLater()
