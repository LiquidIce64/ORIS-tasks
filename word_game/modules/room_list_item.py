from PyQt6.QtWidgets import QWidget

from .gui import Ui_RoomListItem


class RoomListItem(QWidget, Ui_RoomListItem):
    def __init__(self, browser, name: str, player_count: int, max_players: int):
        super().__init__()
        self.setupUi(self)
        self.browser = browser
        self.setStyleSheet(self.browser.main.stylesheet)
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


class ServerRoomListItem(QWidget):
    def __init__(self, server):
        super().__init__()
        self.server = server
        self.setStyleSheet(self.server.main.stylesheet)

        self.players = {}
        self.server.layout_roomlist.addWidget(self)
