from board import Board
from word_bag import ScrabbleBag
from player import Player, Move

class Game:
    def __init__(self, num_players):
        self.passes = 0
        self.no_players = num_players
        self.board = Board()
        self.bag = ScrabbleBag()
        self.game_over = False
        self.player_turn = 0
        self.players = [Player(self.bag) for x in range(num_players)]
        self.skips = 0
        self.move_id = 0

    def check_game_over(self):
        if self.skips > 5:
            self.game_over = True
        for player in self.players:
            if not player.tiles:
                self.game_over = True

    def end_scrabble(self):
        self.board.print()
        print("Scrabble is over. Nice work!")

    def change_turn(self):
        if self.player_turn == self.no_players - 1:
            self.player_turn = 0
        else:
            self.player_turn +=1

    def game_loop(self):
        move_id = 0
        while not self.game_over:
            self.board.print()
            for num, player in enumerate(self.players):
                print('Player {0} with {1} points'.format(str(num + 1), player.score))
            print("Here are your tiles: ")
            self.players[self.player_turn].print_tiles()
            move = Move(move_id)
            move_id += 1
            self.players[self.player_turn].make_move(self.board, move)
            if self.players[self.player_turn].pass_turn:
                self.skips += 1
            else:
                self.players[self.player_turn].score += self.board.calculate_score(move)
                self.skips = 0
            self.check_game_over()
            self.change_turn()

        self.end_scrabble()
