import socket
import json
import base64
import sys


class Client():
    def __init__(self, host, port):
        self.move = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.alive = True
        serv = self.sock.recv(1000)
        name = input(serv).encode('utf-8')
        self.sock.send(name)
        self.start_game()

    def start_game(self):
        while self.alive:
            msg_recv = self.sock.recv(100000)
            print('msg', msg_recv)
            game_res = json.loads(base64.b64decode(msg_recv))
            if 'game_over' in game_res:
                self.alive = False
            self.print_response(game_res)
            if 'board' in game_res:
                self.get_move()
                response = base64.b64encode(json.dumps(self.move
                                                       ).encode('utf-8'))
                self.sock.send(response)
        print('Nice work! Game over')

    def print_response(self, dict):
        for _, value in dict.items():
            print(value)

    def get_inputs(self):
        self.move['letters'] = list(input(
            "What letters do you want to play? ").upper())
        self.move['x'] = input(
            "Where would you like to play in the X direction (1-15)? ")
        self.move['y'] = input(
            "Where would you like to play in the Y direction (1-15) ")
        self.move['direction'] = input(
            "What direction do you want to play in? (across or down) ")

    def get_move(self):
        self.get_inputs()
        while not self.validate_inputs():
            self.get_inputs()

    def validate_inputs(self):
        return True


Client(sys.argv[1], 12355)
