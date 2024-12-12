from threading import Thread
from queue import SimpleQueue
from .networking import ClientServer

from PyQt6.QtCore import QObject, pyqtSignal


class Communication(QObject):
    connect_signal = pyqtSignal(dict)
    host_signal = pyqtSignal(bool)
    recv_signal = pyqtSignal(dict)
    send_queue = SimpleQueue()
    socket = ClientServer()

    def __init__(self):
        super().__init__()
        Thread(target=self.send_messages, daemon=True).start()

    def connect_to_server(self, addr, username: str, password: str):
        try:
            print(self.socket)
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
        try:
            while self.socket.is_open():
                data = self.socket.recv(recipient)
                if recipient is not None: data["from"] = recipient_name
                print(data)
                self.recv_signal.emit(data)
                if data["type"] == "event" and data["event"] == "disconnect":
                    break
        except: return