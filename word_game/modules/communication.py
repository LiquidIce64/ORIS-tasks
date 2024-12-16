from __future__ import annotations

from threading import Thread
from queue import SimpleQueue
from .networking import ClientServer

from PyQt6.QtCore import QObject, pyqtSignal


class Communication(QObject):
    connect_signal = pyqtSignal(dict)
    host_signal = pyqtSignal(bool)
    recv_signal = pyqtSignal(dict)
    send_queue = SimpleQueue()
    socket: ClientServer | None = None

    def __init__(self):
        super().__init__()
        Thread(target=self.send_messages, daemon=True).start()

    def connect_to_server(self, addr, username: str, password: str):
        try:
            self.socket = ClientServer()
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
            self.socket = ClientServer()
            self.socket.host(client_handling_func, *addr)
            self.host_signal.emit(True)
        except:
            self.host_signal.emit(False)

    def send_messages(self):
        while True:
            data = self.send_queue.get()
            try:
                if isinstance(data, dict):
                    self.socket.send(data)
                elif isinstance(data, tuple):
                    self.socket.send(data[0], data[1])
                else:
                    print(f"[WARN] Unknown message type encountered while sending data\nData: {data}")
            except Exception as e: print(f"[WARN] Exception while sending data\nData: {data}\nException: {e.with_traceback(None)}")

    def recv_messages(self, recipient=None, recipient_name=""):
        try:
            while self.socket.is_open():
                data = self.socket.recv(recipient)
                if recipient is not None: data["from"] = recipient_name
                self.recv_signal.emit(data)
                if data["type"] == "event" and data["event"] == "disconnect":
                    break
        except: return
