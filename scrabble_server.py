import asyncio
import base64
import json

from NetworkGame import NetworkGame


class Server():
    def __init__(self, interface, port):
        self.waiting_players = []
        self.games = []
        loop = asyncio.get_event_loop()
        loop.create_task(asyncio.start_server(self.handle_client, '', port))
        loop.run_forever()

    async def handle_client(self, reader, writer):
        response = "Welcome! What's your name?"
        writer.write(response.encode('utf-8'))
        request = (await reader.read(10000))
        print(request)
        self.waiting_players.append((request, reader, writer))
        self.match_players()

    # def get_connections(self):
    #     while True:
    #         player_socket, _ = self.sock.accept()
    #         player_socket.send(b'Welcome! Whats your name?')
    #         buf = player_socket.recv(1000)
    #         name = buf
    #         self.waiting_names.append(name)
    #         self.waiting_players.append(player_socket)
    #         self.match_players()
    def match_players(self):
        while len(self.waiting_players) > 1:
            for player in self.waiting_players[:2]:
                name, _, writer = player
                msg_str = 'Congrats!!! You have been matched with %s' %  \
                    name
                welcome = {'welcome': msg_str}
                msg = base64.b64encode(json.dumps(welcome).encode('utf-8'))
                writer.write(msg)
            game = NetworkGame(self.waiting_players[:2])
            game.game_loop()
            self.waiting_players = self.waiting_players[2:]


Server('', 12355)
