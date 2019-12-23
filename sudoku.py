import math
from string import digits


class Sudoku:

    def __init__(self):
        row, col = 9, 9
        self.board = [[0 for _ in range(col)] for _ in range(row)]  # THIS FEELS DUMB AND BLOATED!

    def print(self):
        s = ""
        for row in self.board:
            for val in row:
                s += str(val) + " "
            s += "\n"
        print(s)

    def load_board(self, board):
        board_list = list(self.extract_board_string(board))
        for row in self.board:
            for j, val in enumerate(row):
                row[j] = int(board_list.pop(0))
        if self.validate_board():
            print("Valid Board loaded!")
            self.print()
            return True
        else:
            print("Inva1lid Board!")
            return False

    def validate_board(self):
        for row, x in enumerate(self.board):
            for col, _ in enumerate(x): # TODO: Determin if i should Replace with Range(len(x))
                if not self.validate_cell(row, col):
                    return False
        return True

    def validate_cell(self, row, col):
        if self.validate_row(row) and self.validate_col(col) and self.validate_box(row, col):
            return True
        else:
            return False

    def __validate(self, list):
        found = []
        for cell in list:
            if cell in found:
                return False
            elif cell != 0:
                found.append(cell)
        return True

    # Iterate over every cell in Row to locate duplicates
    def validate_row(self, row):
        return self.__validate(self.get_row(row))

    # Iterate over every cell in Col to locate duplicates
    def validate_col(self, col):
        return self.__validate(self.get_col(col))

    # validate box
    def validate_box(self, row, col):
        return self.__validate(self.get_box(row, col))

    def get_row(self, row):
        return self.board[row]

    def get_col(self, col):
        return [row[col] for row in self.board]

    # Determine Box, Determine Cell offsets, Return Cells in Box as List
    def get_box(self, row, col):
        box_row = math.ceil((row + 1) / 3)
        box_col = math.ceil((col + 1) / 3)
        box = []
        for r in range(3):
            for c in range(3):
                # row offset, col offset
                rx = (box_row - 1) * 3
                cx = (box_col - 1) * 3
                cell = self.board[r + rx][c + cx]
                box.append(cell)
        return box

    def extract_board_string(self, board):
        s = ''
        for seq in board:
            for c in seq:
                if c in digits:
                    s += c
        return s
