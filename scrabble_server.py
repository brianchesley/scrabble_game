import socket
from NetworkGame import NetworkGame
import base64
import json


class Server():
    def __init__(self, interface, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((interface, port))
        self.sock.listen(1)
        self.waiting_players = []
        self.waiting_names = []
        self.games = []
        self.get_connections()

    def get_connections(self):
        while True:
            player_socket, _ = self.sock.accept()
            player_socket.send(b'Welcome! Whats your name?')
            buf = player_socket.recv(1000)
            name = buf
            self.waiting_names.append(name)
            self.waiting_players.append(player_socket)
            self.match_players()

    def match_players(self):
        if len(self.waiting_players) == 2:
            print('matched!')
            for index, player in enumerate(self.waiting_players):
                name_ind = 1 - index
                msg_str = 'Congrats!!! You have been matched with %s' %  \
                    self.waiting_names[name_ind]
                welcome = {'welcome': msg_str}
                msg = base64.b64encode(json.dumps(welcome).encode('utf-8'))
                player.send(msg)
            game = NetworkGame(self.waiting_names, self.waiting_players)
            game.game_loop()


Server('', 12355)
