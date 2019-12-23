from copy import copy

import sudoku
import boards


class Solver:

    def __init__(self):
        row, col = 9, 9
        self.guesses = [[[] for _ in range(col)] for _ in range(row)]
        self.puzzle = None

    # TODO: Better Fail State/ Exception Handling on Puzzles Failed Load?
    def load_puzzle(self, board):
        self.puzzle = sudoku.Sudoku()
        if self.puzzle.load_board(board):
            print("Sucessfull Load")
            self.populate_all_guesses()
        else:
            print("Failed Load")
            raise Exception('Failure to load puzzle')

    def populate_all_guesses(self):
        for x, row in enumerate(self.guesses):
            for y, cell in enumerate(row):
                if self.puzzle.board[x][y] == 0:
                    self.guesses[x][y] = self.get_cell_guesses(self.puzzle, x, y)

    # DAYYYMM! That's one sexy function. Best refactor ever!
    # TODO: Determinf if this should become a static method
    def get_cell_guesses(self, puzzle, row, col):
        guesses = range(1, 10)
        guesses = [x for x in guesses if x not in puzzle.get_row(row)]
        guesses = [x for x in guesses if x not in puzzle.get_col(col)]
        guesses = [x for x in guesses if x not in puzzle.get_box(row, col)]
        return guesses

    # TODO: Learn Backtracking algorithm
    def solve(self):
        empty = 0
        for row in self.puzzle.board:
            empty += row.count(0)

        self.__solve_dumb(self.puzzle, empty)

    # Smart Recursive Solver (locates lowest guess count)
    def __solve(self, puzzle, guesses):
        pass

    # Dumb Recursive Solver
    def __solve_dumb(self, puzzle, empty):
        print('Solving!')
        if empty <= 0:
            if puzzle.validate_board():
                print(puzzle)
                return True
            return False

        for x, row in enumerate(puzzle.board):
            for y, cell in enumerate(row):
                if cell == 0:
                    guesses = self.get_cell_guesses(puzzle, x, y)
                    puz = copy(puzzle) # Puzzle and Puz are still pointing to the same object,
                    for val in guesses:
                        puz.board[x][y] = val
                        if self.__solve_dumb(puz, empty-1):
                            puzzle = puz
                            return True
                        else:
                            puz.board[x][y] = 0
        return False


s = Solver()
s.load_puzzle(boards.board_easy)
s.solve()
print("Done Run!")


