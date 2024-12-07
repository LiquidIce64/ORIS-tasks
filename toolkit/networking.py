from __future__ import annotations
import typing
import socket
import threading
import pickle


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
        self.__addr: typing.Tuple[str, int] | None = None
        self.__hosting = False
        self.__connected = False
        self._clients: dict | None = None

    def connect(self, address: str = "localhost", port: int = 54321):
        if self.__hosting:
            raise RuntimeError("Can't connect while hosting, use another instance or disconnect first")
        if self.__connected:
            raise RuntimeError("Can't connect to multiple servers")
        self.__addr = (address, port)
        self.__sock.connect(self.__addr)
        self.__connected = True

    def host(self,
             client_handling_func: typing.Callable[[typing.Self, socket.socket, typing.Tuple[str, int]], None],
             address: str = "localhost", port: int = 54321, max_connections: int = -1) -> None:
        if self.__connected:
            raise RuntimeError("Can't host while client is open, use another instance or disconnect first")
        if self.__hosting:
            raise RuntimeError("Can't host multiple servers")
        self._clients = {}
        self.__addr = (address, port)
        self.__sock.bind(self.__addr)
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
                self._clients[addr] = client
                threading.Thread(target=client_handling_func, args=(self, client, addr), daemon=True).start()
        except ConnectionError:
            if self.is_open():
                raise RuntimeError("Server socket closed abruptly")

    def broadcast(self, data: dict):
        if not self.__hosting: return
        for client in self._clients.values():
            self.send(data, client)

    def send(self, data: dict, recipient: socket.socket = None):
        if not self.is_open(): return
        if recipient is None:
            if self.__hosting: return self.broadcast(data)
            recipient = self.__sock
        recipient.send(pickle.dumps(data))

    def recv(self, receiver: socket.socket = None) -> dict | None:
        if not self.is_open(): return
        if receiver is None:
            if self.__hosting:
                if len(self._clients) == 0: return
                receiver = list(self._clients.values())[-1]
            else:
                receiver = self.__sock

        try:
            res = pickle.loads(receiver.recv(self._BUFFER_SIZE))
        except ConnectionError:
            if self.__hosting:
                for k, v in self._clients.items():
                    if v == receiver:
                        self._clients.pop(k)
                        break
            elif self.__connected:
                self.disconnect()
            res = {
                "type": "event",
                "event": "disconnect",
                "body": "connection lost"
            }

        return res

    def disconnect(self):
        if self.__hosting:
            try: self.broadcast({
                "type": "event",
                "event": "disconnect",
                "body": "server closed"
            })
            except: pass
        elif self.__connected:
            try: self.send({
                "type": "event",
                "event": "disconnect",
                "body": "user disconnect"
            })
            except: pass
        self.__addr = None
        self.__hosting = False
        self.__connected = False
        self._clients = None
        self.__sock.close()

    def __repr__(self):
        if self.is_open():
            return f"Open {'Server' if self.__hosting else 'Client'} ({self.__addr[0]}:{self.__addr[1]})"
        return "Closed ClientServer"

    def __del__(self):
        self.disconnect()


if __name__ == '__main__':
    if input("select mode (1-server, 2-client): ") == "1":
        s = ClientServer()

        def handle_client(self: ClientServer, client: socket.socket, address: typing.Tuple[str, int]):
            print("Sending hello")
            self.send(self.str_to_msg("Hello"), client)
            print("Waiting for client")
            print("Received from client:", self.recv(client))

        s.host(handle_client)
        print("Server running")
    else:
        c = ClientServer()
        c.connect()
        print("Connected to server")
        print("Received from server:", c.recv())
        print("Sending hi")
        c.send(c.str_to_msg("hi"))

    input()
