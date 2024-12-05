from __future__ import annotations
from warnings import filterwarnings
from threading import Thread
from toolkit.networking import ClientServer

import gui
from PyQt6.QtCore import pyqtSignal, pyqtSlot, QObject
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget
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


class RoomBrowser(QWidget, gui.Ui_RoomBrowser):  # TODO
    pass


class Communication(QObject):
    connect_signal = pyqtSignal(str)
    host_signal = pyqtSignal(bool)


class Menu(QWidget, gui.Ui_Menu):
    def __init__(self, main_window: Window):
        super().__init__(main_window)
        self.setupUi(self)
        self.main_window = main_window

        self.btn_connect.clicked.connect(self.connect_clicked)
        self.btn_host.clicked.connect(self.host_clicked)

        self.main_window.comm.host_signal.connect(self.host_finished)
        self.main_window.comm.connect_signal.connect(self.connect_finished)

    @pyqtSlot()
    def host_clicked(self):
        addr = parse_address(self.input_address.text())
        self.input_password.setProperty("highlight-incorrect", False)
        self.input_address.setProperty("highlight-incorrect", addr is None)
        self.input_address.setStyleSheet(STYLESHEET)
        if addr is None: return
        Thread(target=self.main_window.host_server, args=(addr,), daemon=True).start()

    @pyqtSlot(bool)
    def host_finished(self, success: bool):
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
        Thread(target=self.main_window.connect_to_server, args=(
            addr,
            self.input_username.text(),
            self.input_password.text()
        ), daemon=True).start()

    @pyqtSlot(str)
    def connect_finished(self, result: str):
        self.setEnabled(True)
        self.btn_connect.setText("Connect")
        self.input_password.setProperty("highlight-incorrect", result == "auth-fail")
        self.input_address.setProperty("highlight-incorrect", result == "timeout")
        self.setStyleSheet(STYLESHEET)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.socket = ClientServer()
        self.comm = Communication()
        self.comm.connect_signal.connect(self.connect_finished)
        self.comm.host_signal.connect(self.host_finished)
        self.menu = Menu(self)
        self.room_browser: RoomBrowser | None = None
        self.server: Server | None = None
        self.setCentralWidget(self.menu)

    def connect_to_server(self, addr, username, password):
        try:
            self.socket.connect(*addr)
            self.socket.send({
                "type": "event",
                "event": "connect",
                "username": username,
                "password": password
            })
            reply = self.socket.recv()
            self.comm.connect_signal.emit(reply["event"])
        except:
            self.comm.connect_signal.emit("timeout")

    @pyqtSlot(str)
    def connect_finished(self, result: str):
        if result != "accepted": return
        self.room_browser = RoomBrowser()
        self.setCentralWidget(self.room_browser)

    def host_server(self, addr):
        try:
            self.server = Server()
            self.socket.host(self.server.handle_connection, *addr)
            self.comm.host_signal.emit(True)
        except:
            self.server = None
            self.comm.host_signal.emit(False)

    @pyqtSlot(bool)
    def host_finished(self, success: bool):
        if success:
            self.setCentralWidget(self.server)


app = QApplication([])
app.setStyleSheet(STYLESHEET)
window = Window()
window.show()
app.exec()
