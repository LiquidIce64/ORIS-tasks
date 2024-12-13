from __future__ import annotations
import typing
import socket
import threading
import pickle


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


class ClientServer:
    _BUFFER_SIZE = 1024

    @staticmethod
    def str_to_msg(s: str) -> dict:
        return {
            "type": "msg",
            "len": len(s),
            "msg": s
        }

    def __init__(self):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__hosting = False
        self.__connected = False

    def connect(self, address: str = "localhost", port: int = 54321):
        if self.__hosting:
            raise RuntimeError("Can't connect while hosting, use another instance or disconnect first")
        if self.__connected:
            raise RuntimeError("Can't connect to multiple servers")
        self.__sock.connect((address, port))
        self.__connected = True

    def host(self,
             client_handling_func: typing.Callable[[typing.Self, socket.socket, typing.Tuple[str, int]], None],
             address: str = "localhost", port: int = 54321, max_connections: int = -1) -> None:
        if self.__connected:
            raise RuntimeError("Can't host while client is open, use another instance or disconnect first")
        if self.__hosting:
            raise RuntimeError("Can't host multiple servers")
        self.__sock.bind((address, port))
        if max_connections != -1:
            self.__sock.listen(max_connections)
        else:
            self.__sock.listen()
        self.__hosting = True
        threading.Thread(target=self.__accept_connections, args=(client_handling_func,), daemon=True).start()

    def is_open(self):
        return self.__connected or self.__hosting

    def __accept_connections(self, client_handling_func: typing.Callable[[typing.Self, socket.socket, typing.Tuple[str, int]], None]):
        try:
            while self.is_open():
                client, addr = self.__sock.accept()
                threading.Thread(target=client_handling_func, args=(self, client, addr), daemon=True).start()
        except:
            if self.is_open():
                raise RuntimeError("Server socket closed abruptly")

    def send(self, data: dict, recipient: socket.socket = None):
        if not self.is_open(): return
        if recipient is None:
            if self.__hosting: return
            recipient = self.__sock
        recipient.send(pickle.dumps(data))
        if data["type"] == "event" and data["event"] == "disconnect":
            recipient.close()

    def recv(self, receiver: socket.socket = None) -> dict | None:
        if not self.is_open(): return
        if receiver is None:
            if self.__hosting: return
            receiver = self.__sock

        try:
            res = pickle.loads(receiver.recv(self._BUFFER_SIZE))
        except:
            if self.__hosting:
                receiver.close()
            elif self.__connected:
                self.disconnect()
            res = {
                "type": "event",
                "event": "disconnect",
                "body": "Connection lost"
            }

        return res

    def disconnect(self):
        if self.__connected:
            try: self.send({
                "type": "event",
                "event": "disconnect",
                "body": "User disconnect"
            })
            except: pass
        self.__hosting = False
        self.__connected = False
        self.__sock.close()

    def __repr__(self):
        if self.is_open():
            return f"Open {'Server' if self.__hosting else 'Client'} ({self.__addr[0]}:{self.__addr[1]})"
        return "Closed ClientServer"

    def __del__(self):
        self.disconnect()
