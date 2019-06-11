from board import Board
from player import Player, Move
from word_bag import ScrabbleBag


class NetworkGame():
    def __init__(self, names, sockets, num_players=2):
        # TODO refactor game base class for use in network and use locally
        self.passes = 0
        self.no_players = num_players
        self.board = Board()
        self.bag = ScrabbleBag()
        self.game_over = False
        self.player_turn = 0
        self.players = [Player(self.bag, name, socket) for name, socket in
                        zip(names, sockets)]
        self.skips = 0
        self.move_id = 0
        self.game_data = {}
        self.local = True
        if sockets:
            self.local = False

    def check_game_over(self):
        if self.skips > 5:
            self.game_over = True
        for player in self.players:
            if not player.tiles:
                self.game_over = True

    def end_scrabble(self):
        msg = "Scrabble is over! Good work."
        board = self.board.to_str()
        if self.local:
            print(board)
            print(msg)
        else:
            for player in self.players:
                player.send_msg(msg)
                player.send_msg(self.game_data)
        print("Scrabble is over. Nice work!")

    def change_turn(self):
        if self.player_turn == self.no_players - 1:
            self.player_turn = 0
        else:
            self.player_turn += 1

    def game_loop(self):
        move_id = 0
        while not self.game_over:
            self.game_data['board'] = self.board.to_str()
            self.game_data['player'] = ''
            for player in self.players:
                self.game_data['player'] += 'Player {0} with {1} points' \
                    .format(player.name, player.score)
                self.game_data['player'] += "\n"
            tile_str = "Here are your tiles: "
            tile_str += self.players[self.player_turn].print_tiles()
            self.game_data['tiles'] = tile_str
            move = Move(move_id, self.players[self.player_turn].tiles)
            self.players[self.player_turn].get_move(move, self.game_data)
            self.players[self.player_turn].make_move(self.board, move)
            move_id += 1
            if self.players[self.player_turn].pass_turn:
                self.skips += 1
            else:
                self.players[self.player_turn].score += \
                    self.board.calculate_score(move)
                self.skips = 0
            self.check_game_over()
            self.change_turn()
        self.end_scrabble()
