from scrabble_config import POINT_MAPPING
from word_bag import Letter


class ScrabbleBoard:
    SCRABBLE_BOARD = [
        ['3W', '', '', '2L', '', '', '', '3W', '', '', '', '2L', '', '', '3W'],
        ['', '2W', '', '', '', '3L', '', '', '', '3L', '', '', '', '2W', ''],
        ['', '', '2W', '', '', '', '2L', '', '2L', '', '', '', '2W', '', ''],
        ['2L', '', '', '2W', '', '', '', '2L', '', '', '', '2W', '', '', '2L'],
        ['', '', '', '', '2W', '', '', '', '', '', '2W', '', '', '', ''],
        ['', '3L', '', '', '', '3L', '', '', '', '3L', '', '', '', '3L', ''],
        ['', '', '2L', '', '', '', '2L', '', '2L', '', '', '', '2L', '', ''],
        ['3W', '', '', '2L', '', '', '', '2W', '', '', '', '2L', '', '', '3W'],
        ['', '', '2L', '', '', '', '2L', '', '2L', '', '', '', '2L', '', ''],
        ['', '3L', '', '', '', '3L', '', '', '', '3L', '', '', '', '3L', ''],
        ['', '', '', '', '2W', '', '', '', '', '', '2W', '', '', '', ''],
        ['2L', '', '', '2W', '', '', '', '2L', '', '', '', '2W', '', '', '2L'],
        ['', '', '2W', '', '', '', '2L', '', '2L', '', '', '', '2W', '', ''],
        ['', '2W', '', '', '', '3L', '', '', '', '3L', '', '', '', '2W', ''],
        ['3W', '', '', '2L', '', '', '', '3W', '', '', '', '2L', '', '', '3W']
                      ]


class BoardTile(Letter):
    def __init__(self, type, x, y):
        super(BoardTile, self).__init__(None)
        self.type = type
        self.empty = True
        self.move_id = None
        self.x = x
        self.y = y

    def play_tile(self, letter, move_id):
        self.char = letter.char
        self.empty = False
        self.move_id = move_id

    def remove_tiles(self, letter, move_id):
        self.char = None
        self.move_id = None
        self.empty = True


    def __repr__(self):
        if self.char:
            return self.char + " "
        elif self.type:
            return self.type
        else:
            return "__"


class Board(ScrabbleBoard):
    def __init__(self):
        self.board = [[] for _ in range(15)]
        for row_ind, row in enumerate(self.SCRABBLE_BOARD):
            for col_ind, col_val in enumerate(row):
                tile = BoardTile(col_val, col_ind, row_ind)
                self.board[row_ind].append(tile)

    def calculate_col_score(self, move, secondary=False):
        col = [row[move.x] for row in self.board]
        start = self.word_start(col, move.y)
        end = self.word_end(col, move.y)
        if secondary:
            if end - start == 0:
                return 0
        score = self.score_word(col, start, end, move.move_id)
        return score

    def word_start(self, slice, ind):
        start = ind
        while not slice[start].empty:
            start -= 1
        return start + 1

    def word_end(self, slice, ind):
        end = ind
        while not slice[end].empty:
            end += 1
        return end - 1

    def calc_row_score(self, move, secondary=False):
        row = self.board[move.y]
        start = self.word_start(row, move.x)
        end = self.word_end(row, move.x)
        if secondary:
            if end - start == 0:
                return 0
        score = self.score_word(row, start, end, move.move_id)
        return score

    def score_word(self, slice, start, end, move_id):
        score = 0
        word_multi = 1
        for i in range(start, end + 1):
            char_multi = 1
            if slice[i].type in ['3L', '2L'] and slice[i].move_id == move_id:
                char_multi = int(slice[i].type[0])
                slice[i].type == ''
                print('hello')
            elif slice[i].type in ['3W', '2W'] and slice[i].move_id == move_id:
                word_multi = word_multi * int(slice[i].type[0])
                slice[i].type == ''
            score += POINT_MAPPING[slice[i].char] * char_multi
        return score * word_multi

    def place_tiles(self, move, remove=False):
        tile_ind = 0
        board_ind = 0
        while tile_ind < len(move.tiles_move):
            if move.direction == 'across':
                start = move.x
                if self.board[move.y][board_ind + start].empty:
                    self.board[move.y][board_ind + start].play_tile(move.tiles_move[tile_ind], move.move_id)
                    tile_ind += 1
                board_ind += 1
            elif move.direction == 'down':
                start = move.y
                if self.board[board_ind + start][move.x].empty:
                    self.board[board_ind + start][move.x].play_tile(move.tiles_move[tile_ind], move.move_id)
                    tile_ind += 1
                board_ind += 1


    def calculate_score(self, move):
        if move.direction == 'across':
            score_across = self.calc_row_score(move, False)
            score_down = 0
            for tile in self.board[move.y][move.x:]:
                if tile.move_id == move.move_id:
                    score_down += self.calculate_col_score(tile.x, tile.y, True)

        elif move.direction == 'down':
            score_down = self.calculate_col_score(move.x, move.y, False)
            score_across = 0
            for y in range(move.y, 15):
                if self.board[y][move.x].move_id == move.move_id:
                    score_across += self.calc_row_score(move.x, move.y, True)
        return score_across + score_down

        return score

    def check_start(self, move):
        if self.board[move.y][move.x].empty:
            return True
        else:
            return False

    def open_tiles(self, move):
        if move.direction == 'across':
            start = move.x
            free_tiles = [b_tile.empty for b_tile in self.board[move.y][start:]]
        elif move.direction == 'down':
            free_tiles = [row[move.x].empty for row in self.board]
        if len(move.tiles_move) > sum(free_tiles):
            print("There are not enough open tiles for this play ")
            return False
        return True

    def check_middle(self, move):
        if move.direction == 'across' and move.y == 7:
            if 7 in range(move.x, move.x + len(move.tiles_move)):
                return True
        if move.direction == 'down' and move.x == 7:
            if 7 in range(move.y, move.y + len(move.tiles_move)):
                return True
        return False

    def anchor_tile(self, move):
        if move.direction == 'across':
            start = move.x - 1
            if start < 0:
                start = 0
            end = start + len(move.tiles_move) + 1
            if end > 14:
                end = 14
            domain = [x.empty for x in self.board[move.y][start:end]]
        elif move.direction == 'down':
            if move.x == 1:
                start = 0
            else:
                start = move.x - 1
            end = start + len(move.tiles_move) + 1
            if end > 14:
                end = 14
            domain = [row[move.x].empty for row in self.board][start:end]
        if self.check_middle(move):
            return True
        if sum(domain) == len(domain):
            print("There is no anchor tile for this play. ")
            return False
        return True

    def valid_row(self, row):
        curr_word = ''
        for tile in row:
            if not tile.empty:
                curr_word += tile.char
            else:
                if len(curr_word) > 1:
                    if not Utils.word_check(curr_word):
                        print("Sorry {0} is not a word".format(curr_word))
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
        if self.open_tiles(move) and self.anchor_tile(move) and self.check_start(move):
            self.place_tiles(move)
            if self.check_words():
                return True
            else:
                self.place_tiles(move, remove=True)
                return False

    def print(self):
        for ind, row in enumerate(self.board):
            print(15 - ind, row)
        # print(" ",[x for x in range(1,16)]) maybe implement these as tiles?


class Utils:
    def word_check(word):
        if word.upper() in open('./word_dict.txt').read():
            return True

