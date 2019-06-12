from word_bag import Letter, PlayerBag
import json
import base64


class Move:
    def __init__(self, move_id, player_bag):
        self.tiles_move = []
        self.coords = None
        self.direction = None
        self.diff = None
        self.x = None
        self.letters = None
        self.y = None
        self.move_id = move_id
        self.player_bag = player_bag

    def invert_y(self, y):
        return 14 - y

    def get_inputs(self):
        self.tiles_move = []
        self.letters = input("What letters do you want to play? ").upper()
        self.x = input(
            "Where would you like to play in the X direction (1-15)? ")
        self.y = input(
            "Where would you like to play in the Y direction (1-15) ")
        self.direction = input(
            "What direction do you want to play in? (across or down) ")

    def build_move(self, struct):
        # This builds a move from a dictionary from a network
        try:
            self.x = int(struct['x']) - 1
            self.y = self.invert_y(int(struct['y']) - 1)
        except (ValueError, TypeError):
            self.x = None
            self.y = None
        self.letters = struct['letters']
        self.direction = struct['direction']

    def validate_inputs(self):
        if not self.letters and (self.x or self.y):
            return True
        if self.x not in range(15) and self.y not in range(15):
            message = "Please enter a valid place to play. "
            return False
        if self.direction not in ['down', 'across']:
            message = "Please enter a valid direction. "
            return False
        if not self.validate_tiles():
            message = "You don't have these tiles"
            return False
        return True

    def validate_tiles(self):
        player_letters = [x.char for x in self.player_bag]
        diff = [letter in player_letters for letter in list(self.letters)]
        if all(diff):
            return True
        if player_letters.count("?") == diff.count(False):
            return True
        return False

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
    def __init__(self, word_bag, name, socket=None):
        super(Player, self).__init__(7, word_bag)
        self.score = 0
        self.pass_turn = False
        self.socket = socket
        self.name = name

    def get_move(self, move, game_data):
        while not move.validate_inputs():
            if self.socket:
                self.socket.send(base64.b64encode(json.dumps(
                    game_data).encode('utf-8')))
                # TODO add message here saying their move wasn't valid
                resp = json.loads(base64.b64decode(self.socket.recv(10000)))
                move.build_move(resp)
            else:
                move.get_inputs()
        move.create_tiles()

    def make_move(self, move, board, game_data):
        if move.pass_move():
            self.pass_turn = True
        else:
            while not board.valid_move(move):
                move_id = move.move_id
                move = Move(move_id, self.tiles)
                self.get_move(move, game_data)
            self.pass_turn = False
            self.play_draw_tiles(move)

    def print_tiles(self):
        return " ".join(map(str, self.tiles))

    def send_msg(self, message):
        if self.socket:
            self.socket.send(base64.b64encode(json.dumps(message)))
        else:
            print(message)
