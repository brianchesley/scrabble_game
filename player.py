from board import Board
from word_bag import Letter, PlayerBag, ScrabbleBag


class Move:
    def __init__(self, move_id):
        self.tiles_move = []
        self.coords = None
        self.direction = None
        self.diff = None
        self.x = None
        self.letters = None
        self.y = None
        self.move_id = move_id

    def invert_y(self, y):
        return 14 - y

    def get_move(self):
        self.letters = input("What letters do you want to play?")
        self.x = int(input("Where would you like to play in the X direction (1-15)? ")) - 1
        self.y = self.invert_y(int(input("Where would you like to play in the Y direction (1-15) ")) - 1)
        self.direction = input("What direction do you want to play in? (across or down) ")
        while not self.validate_inputs():
            pass
        self.create_tiles()

    def validate_inputs(self):
        if self.x and self.y not in range(1,16):
            print("Please enter a valid place to play. ")
            self.x = int(input("Where would you like to play in the X direction (1-15)? ")) - 1
            self.y = self.invert_y(int(input("Where would you like to play in the Y direction (1-15) ")) - 1)
        if self.direction not in ['down','across']:
            print("Please enter a valid direction. ")
            self.direction = input("What direction do you want to play in? (across or down) ")
        #TODO implement a way to check for valid letters
        return True

    def create_tiles(self):
        for letter in self.letters:
            tile = Letter(letter)
            self.tiles_move.append(tile)

    def pass_move(self):
        if not self.letters:
            return True
        else:
            return False


class Player(PlayerBag):
    def __init__(self, word_bag):
        super(Player, self).__init__(7, word_bag)
        self.score = 0
        self.pass_turn = False

    def make_move(self, board, move):
        move.get_move()
        if move.pass_move():
            self.pass_turn = True
        else:
            self.pass_turn = False
            while not board.valid_move(move):
                move.get_move()
            self.play_draw_tiles(move)

    def print_tiles(self):
        print(self.tiles)


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

