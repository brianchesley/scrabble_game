from board import LetterBag


class Move():
    def __init__(self):
        self.tiles = None
        self.coords = None
        self.direction = None
        self.diff = None

    def get_move(self):
        self.tiles = input("What letters do you want to play?")
        self.coords = [x - 1 for x in input("Where would you like to play?")]
        self.direction = input("What direction do you want to play in?")

    def move_range(self):
        if self.direction == 'across':
            start = self.coords[0]
            end = start + len(self.tiles)
        elif self.direction == 'down':
            start = self.coords[1]
            end = start + len(self.tiles)
        return range(start, end)


class Player(LetterBag, Move):
    def __init__(self):
        super(Player, self,).__init__(LetterBag.draw_tiles(self, 7))

    def make_move(self, ):
        pass

    def parse_move(self):
        pass






