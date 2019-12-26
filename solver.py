import copy
import timeit
import sudoku
import math


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

    # TODO: Determine if this should become a static method
    @staticmethod
    def get_cell_guesses(puzzle, row, col):
        guesses = list(range(1, 10))
        guesses = [x for x in guesses if x not in puzzle.get_row(row)]
        guesses = [x for x in guesses if x not in puzzle.get_col(col)]
        guesses = [x for x in guesses if x not in puzzle.get_box(row, col)]
        return guesses

    # TODO: Refactor update_gueses_by_cell to not reuse code from sudoku class
    @staticmethod
    def update_guesses_by_cell(guesses, puzzle, row, col):
        val = puzzle.board[row][col]
        for i, cell in enumerate(guesses[row]):
            guesses[row][i] = [x for x in cell if x != val]

        for i, cell in enumerate([row[col] for row in guesses]):
            guesses[i][col] = [x for x in cell if x != val]

        box_row = math.ceil((row + 1) / 3)
        box_col = math.ceil((col + 1) / 3)
        for r in range(3):
            for c in range(3):
                # row offset, col offset
                rx = (box_row - 1) * 3
                cx = (box_col - 1) * 3
                cell = guesses[r + rx][c + cx]
                guesses[r + rx][c + cx] = [x for x in cell if x != val]
        return guesses

    def solve(self):
        empty = 0
        for row in self.puzzle.board:
            empty += row.count(0)

        start = timeit.default_timer()
        print('Empty spaces to calculate: ', empty)
        if self.__solve(self.puzzle, self.guesses, empty):
            print("I SOLVED IT!!!!")
            stop = timeit.default_timer()
            print('Time: ', stop-start)
        else:
            print('Awwwww no solution found!')

    # TODO: Refactor __solve alrorithm to be cleaner and more concise
    # Smart Recursive Solver (locates lowest guess count)
    def __solve(self, puzzle, guesses, empty, depth=0):
        if empty <= 0:
            if puzzle.validate_board():
                puzzle.print()
                return True
            return False

        # Get Cell to work on (check guesses for cell with least possibilities)
        row, col = self.__find_best_cell_row_col(guesses)
        possibilities = guesses[row][col]
        tmp_puzzle = copy.deepcopy(puzzle)
        for val in possibilities:
            tmp_puzzle.board[row][col] = val
            # DISGUSTING! Hate having to copy guesses every loop...
            # Data is lost when updating guesses -> Need to re-copy original guesses each try
            tmp_guesses = copy.deepcopy(guesses)
            self.update_guesses_by_cell(tmp_guesses, tmp_puzzle, row, col)
            tmp_guesses[row][col] = []
            print('.' * depth + "Depth: {} - {},{} - Val: {}, {}".format(depth, row, col, val, possibilities))
            if self.__solve(tmp_puzzle, tmp_guesses, empty - 1, depth + 1):
                puzzle = tmp_puzzle
                guesses = tmp_guesses
                return True
            else:
                print('.' * depth + "Failed Path!")
                tmp_puzzle.board[row][col] = 0
        return False

    @staticmethod
    def __find_best_cell_row_col(guesses):
        # [Guess Count, row, col)
        best_cell = [9, 0, 0]
        for x, row in enumerate(guesses):
            for y, cell in enumerate(row):
                if type(cell) is not None and len(cell) > 0:
                    if best_cell is None: best_cell = [len(cell), x, y]
                    if len(cell) < best_cell[0]: best_cell = [len(cell), x, y]
                    if len(cell) == 1: return x, y
        return best_cell[1], best_cell[2]
