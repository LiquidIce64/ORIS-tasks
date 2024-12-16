from typing import TYPE_CHECKING

from threading import Thread
from .networking import parse_address

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QWidget

from .server import Server
from .gui import Ui_Menu, STYLESHEET

if TYPE_CHECKING:
    from .window import Window


class Menu(QWidget, Ui_Menu):
    def __init__(self, main: "Window"):
        super().__init__()
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
        self.setStyleSheet(STYLESHEET)
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
        self.input_address.setProperty("highlight-incorrect", result["event"] != "connect")
        self.setStyleSheet(STYLESHEET)
