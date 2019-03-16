import random
from scrabble_config import POINT_MAPPING
import enchant

class Letter():
    def __init__(self, letter, val):
        self.value = val
        self.char = letter

    def __repr__(self):
        print(self.char, self.value)

class ScrabbleBag(Letter):
    SCRABBLE_LETTERS = [' ', ' ', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'A', 'A', 'A', 'A', 'A', 'A', 'A',
                    'A', 'A', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'N', 'N',
                    'N', 'N', 'N', 'N', 'R', 'R', 'R', 'R', 'R', 'R', 'T', 'T', 'T', 'T', 'T', 'T', 'L', 'L', 'L', 'L', 'S',
                    'S', 'S', 'S', 'U', 'U', 'U', 'U', 'D', 'D', 'D', 'D', 'G', 'G', 'G', 'B', 'B', 'C', 'C', 'M', 'M', 'P',
                    'P', 'F', 'F', 'H', 'V', 'V', 'W', 'W', 'Y', 'Y', 'K', 'J', 'X', 'Q', 'Z']
    scrabble_letters = []
    for letter in SCRABBLE_LETTERS:
        letter = Letter(letter, POINT_MAPPING[letter])
        scrabble_letters.append(letter)

class ScrabbleBoard():
    SCRABBLE_BOARD = [
        ['3W', '', '', '2L', '', '', '', '3W', '', '', '', '2L', '', '', '3W'],
        ['', '2W', '', '', '', '3L', '', '', '', '3L', '', '', '', '2W', ''],
        ['2L', '', '', '2W', '', '', '', '2L', '', '', '', '2W', '', '', '2L'],
        ['', '', '', '', '2W', '', '', '', '', '', '2W', '', '', '', ''],
        ['', '3L', '', '', '', '3L', '', '', '', '3L', '', '', '', '3L', ''],
        ['', '', '2L', '', '', '', '2L', '', '2L', '', '', '', '2L', '', ''],
        ['3W', '', '', '2L', '', '', '', '2W', '', '', '', '2L', '', '', '3W'],
        ['', '', '2L', '', '', '', '2L', '', '2L', '', '', '', '2L', '', ''],
        ['', '3L', '', '', '', '3L', '', '', '', '3L', '', '', '', '3L', ''],
        ['', '', '', '', '2W', '', '', '', '', '', '2W', '', '', '', ''],
        ['2L', '', '', '2W', '', '', '', '2L', '', '', '', '2W', '', '', '2L'],
        ['', '2W', '', '', '', '3L', '', '', '', '3L', '', '', '', '2W', ''],
        ['3W', '', '', '2L', '', '', '', '3W', '', '', '', '2L', '', '', '3W']
                      ]


class LetterBag(ScrabbleBag):
    def __init__(self, tiles):
        self.tiles = tiles

    def draw_tiles(self, num):
        random.shuffle(self.scrabble_letters)
        draw = self.scrabble_letters[0:num]
        self.scrabble_letters = self.scrabble_letters[num:]
        return draw


class BoardTile(Letter):
    def __init__(self, type):
        self.type = type
        self.empty = True

    def play_tile(self, letter):
        self.value = letter.value
        self.char = letter.char
        self.empty = False


class Board(ScrabbleBoard):
    def __init__(self):
        self.board = [[] for _ in range(15)]
        for index, row in enumerate(self.board):
            for col_val in self.SCRABBLE_BOARD[index]:
                tile = BoardTile(col_val)
                row.append(tile)

    def place_tiles(self, move):
        if move.direction == 'across':
            start = move.coords[0]
            tile_ind = 0
            while tile_ind < len(move.tiles):
                if move.direction == 'across':
                    if self.board[move.coords[1]][tile_ind + start].empty:
                        self.board[move.coords[1]][tile_ind + start] = move.tiles[tile_ind]
                        tile_ind += 1
                elif move.direction == 'down':
                    if self.board 

            for index in range(len(move.tiles)):
                y_pos = index + move.coords[1]
                self.board[y_pos][move.coords[0]] = move.tiles[index]

    def open_tiles(self, move):
        if move.direction == 'across':
            start = move.coords[0]
            end = start + len(move.tiles)
            free_tiles = [x.char for x in self.board[move.coords[1]][start:]]
        elif move.direction == 'down':
            free_tiles = [row[move.coords[0]] for row in self.board]
        if len(move.tiles) > sum(free_tiles):
            return 'Not a valid move'

    def anchor_tile(self, move):
        if move.direction == 'across':
            start = move.coords[0] - 1
            if start < 0:
                start = 0
            end = start + len(move.tiles) + 1
            if end > 14:
                end = 14
            domain = [x.empty for x in self.board[move.coords[1]][start:end]]
        elif move.direction == 'down':
            if move.coords[0] == 1:
                start = 0
            else:
                start = move.coords[0] - 1
            end = start + len(move.tiles) + 1
            if end > 14:
                end = 14
            domain = [row[move.coords[0]] for row in self.board]
        if sum(domain) == len(domain):
            if 7 not in move.move_range():
                return 'Not a valid move'
        return True

    def valid_row(self, row):
        d = enchant.Dict("en_US")
        curr_word = ''
        for tile in row:
            if not tile.empty:
                curr_word += tile.char
            else:
                if len(curr_word) > 0:
                    if not d.check(curr_word):
                        return False
                    else:
                        curr_word = ''
        return True

    def check_words(self):
        for row in self.board:
            if not self.valid_row(row):
                return False
        for column in range(15):
            col = [row[column] for row in self.board]
            if not self.valid_row(col):
                return False
        return True

    def valid_move(self, move):
        if self.open_tiles(move) and self.anchor_tile(move) and self.check_words():
            return True
        return False








    def print(self):
        for row in self.board:
            print(*row)
