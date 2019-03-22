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

    def get_inputs(self):
        self.tiles_move = []
        self.letters = input("What letters do you want to play? ").upper()
        self.x = input("Where would you like to play in the X direction (1-15)? ")
        self.y = input("Where would you like to play in the Y direction (1-15) ")
        self.direction = input("What direction do you want to play in? (across or down) ")

    def get_move(self):
        self.get_inputs()
        while not self.validate_inputs():
            self.get_inputs()
        self.create_tiles()

    def validate_inputs(self):
        try:
            self.x = int(self.x) - 1
            self.y = self.invert_y(int(self.y) - 1)
        except ValueError:
            print("Please enter a valid number. ")
            return False
        if self.x and self.y not in range(15):
            print("Please enter a valid place to play. ")
            return False
        if self.direction not in ['down','across']:
            print("Please enter a valid direction. ")
            return False
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
                print("Sorry, not a valid move. Try again. ")
                move.get_move()
            self.play_draw_tiles(move)

    def print_tiles(self):
        print(self.tiles)




