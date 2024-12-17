from __future__ import annotations

from threading import Thread

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QMainWindow, QWidget

from .communication import Communication
from .menu import Menu
from .room_browser import RoomBrowser
from .room import Room
from .server import Server


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.default_parent = QWidget()
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
        self.centralWidget().setParent(self.default_parent)
        self.setCentralWidget(self.room_browser)

    @pyqtSlot(bool)
    def host_finished(self, success: bool):
        if success:
            self.centralWidget().setParent(self.default_parent)
            self.setCentralWidget(self.server)
        else:
            self.server.deleteLater()

    def join_room(self, name: str, max_players: int, player_list: list[dict]):
        self.room = Room(self, name, max_players, player_list)
        self.centralWidget().setParent(self.default_parent)
        self.setCentralWidget(self.room)

    def leave_room(self):
        self.room_browser.refresh()
        self.centralWidget().setParent(self.default_parent)
        self.setCentralWidget(self.room_browser)
        if self.room is not None: self.room.deleteLater()

    @pyqtSlot()
    def exit_to_menu(self):
        self.centralWidget().setParent(self.default_parent)
        self.setCentralWidget(self.menu)
        if self.room is not None: self.room.deleteLater()
        if self.room_browser is not None: self.room_browser.deleteLater()
        if self.server is not None: self.server.deleteLater()
        Thread(target=self.comm.socket.disconnect, daemon=True).start()
