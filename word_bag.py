import random


class Letter:
    def __init__(self, letter):
        self.char = letter

    def __repr__(self):
        if self.char is not None:
            return self.char + " "
        else:
            return "__"

    def __eq__(self, other):
        return self.char == other.char


class ScrabbleBag(Letter):
    SCRABBLE_LETTERS = ['?', '?', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'A', 'A', 'A', 'A', 'A',
                        'A', 'A', 'A', 'A', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'O', 'O', 'O', 'O', 'O', 'O',
                        'N', 'N', 'N', 'N', 'R', 'R', 'R', 'R', 'R', 'R', 'T', 'T', 'T', 'T', 'T', 'T', 'L', 'L', 'L',
                        'L', 'S', 'S', 'S', 'S', 'U', 'U', 'U', 'U', 'D', 'D', 'D', 'D', 'G', 'G', 'G', 'B', 'B', 'C',
                        'C', 'M','M', 'P', 'P', 'F', 'F', 'H', 'V', 'V', 'W', 'W', 'Y', 'Y', 'K', 'J', 'X', 'Q', 'Z']

    def __init__(self):
        self.scrabble_bag = self.make_bag()

    def make_bag(self):
        scrabble_letters = []
        for letter in self.SCRABBLE_LETTERS:
            letter = Letter(letter)
            scrabble_letters.append(letter)
        return scrabble_letters

    def draw_tiles(self, num):
        random.shuffle(self.scrabble_bag)
        if num > len(self.scrabble_bag):
            draw = self.scrabble_bag
        else:
            draw = self.scrabble_bag[0:num]
            self.scrabble_bag = self.scrabble_bag[num:]
        return draw


class PlayerBag:
    def __init__(self, num_tiles, bag):
        self.tiles = bag.draw_tiles(num_tiles)
        self.bag = bag

    def play_draw_tiles(self, move):
        print(self.tiles)
        for let in move.tiles_move:
            try:
                self.tiles.remove(let)
            except ValueError:
                self.tiles.remove('?')
        self.tiles = self.tiles + self.bag.draw_tiles(len(move.tiles_move))
