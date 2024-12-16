from typing import TYPE_CHECKING

from PyQt6.QtCore import QObject, QTimer, pyqtSlot

if TYPE_CHECKING:
    from .room_list_item import ServerRoomListItem


class Game(QObject):
    def __init__(self, room: "ServerRoomListItem"):
        super().__init__()
        self.room = room
        self.players = list(self.room.players.keys())
        self.current_player_ind = -1
        self.used_words: list[str] = []

        self.turn_timer = QTimer()
        self.turn_timer.timeout.connect(self.out_of_time)

        self.next_turn()

    @pyqtSlot()
    def out_of_time(self):
        username = self.players[self.current_player_ind]
        self.room.server.main.comm.send_queue.put(({
            "type": "event",
            "event": "kick",
            "body": "Out of time"
        }, self.room.server.clients[username]))
        self.room.server.leave_room(username)

    def remove_player(self, username):
        ind = self.players.index(username)
        if ind < self.current_player_ind:
            self.current_player_ind -= 1
            self.players.remove(username)
        elif ind > self.current_player_ind:
            self.players.remove(username)
        else:
            self.current_player_ind -= 1
            self.players.remove(username)
            self.next_turn()

    def submit_word(self, word: str, from_username: str):
        if from_username != self.players[self.current_player_ind]: return

        word = word.strip()
        if len(word) == 0: return
        word_lower = word.lower()
        if word_lower in self.used_words: return
        if self.used_words and not word_lower.startswith(self.used_words[-1][-1]): return

        self.used_words.append(word_lower)

        self.next_turn(word)

    def next_turn(self, word: str = None):
        self.turn_timer.stop()
        self.current_player_ind += 1
        if self.current_player_ind >= len(self.players):
            self.current_player_ind -= len(self.players)

        turn_info = {"player": self.players[self.current_player_ind]}
        if word is not None: turn_info["word"] = word
        self.room.broadcast({
            "type": "event",
            "event": "turn",
            "body": turn_info
        })
        self.turn_timer.start(30000)

    def deleteLater(self):
        self.turn_timer.stop()
        self.room.game = None
        super().deleteLater()
