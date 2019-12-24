import copy
import sudoku
import boards
import math


# TODO: Move all guesses logic into Sudoku class.....
# This is dumb the amount of janky solutions so similar to the puzzle board logic


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
        guesses = list(range(1, 10))
        guesses = [x for x in guesses if x not in puzzle.get_row(row)]
        guesses = [x for x in guesses if x not in puzzle.get_col(col)]
        guesses = [x for x in guesses if x not in puzzle.get_box(row, col)]
        return guesses

    # Oh god, send help!. This is turning into a clusterfuck...
    def update_guesses_by_cell(self, guesses, puzzle, row, col):
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

    # TODO: Learn Backtracking algorithm
    def solve(self):
        empty = 0
        for row in self.puzzle.board:
            empty += row.count(0)

        print(empty)
        # self.__solve_dumb(self.puzzle, empty)
        if self.__solve(self.puzzle, self.guesses, empty):
            print("I SOLVED IT!!!!")
        else:
            print('Awwwww no solution found!')

    # Smart Recursive Solver (locates lowest guess count)
    def __solve(self, puzzle, guesses, empty, depth=0):
        if empty <= 0:
            if puzzle.validate_board():
                print(puzzle)
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

    # Find cell with least options (Guess count)
    def __find_best_cell_row_col(self, guesses):
        # [Guess Count, row, col)
        best_cell = [9, 0, 0]
        for x, row in enumerate(guesses):
            for y, cell in enumerate(row):
                if type(cell) is not None and len(cell) > 0:
                    if best_cell is None: best_cell = [len(cell), x, y]
                    if len(cell) < best_cell[0]: best_cell = [len(cell), x, y]
                    if len(cell) == 1: return x, y
        return best_cell[1], best_cell[2]

    # Dumb Recursive Solver
    # Unable to tell if valid, CBF letting it run for long enough to see if it finds a valid solution
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
                    puz = copy.deepcopy(puzzle)  # Puzzle and Puz are still pointing to the same object,
                    for val in guesses:
                        puz.board[x][y] = val
                        if self.__solve_dumb(puz, empty - 1):
                            puzzle = puz
                            return True
                        else:
                            puz.board[x][y] = 0
        return False


s = Solver()
s.load_puzzle(boards.board_evil2)
s.solve()
print("Done Run!")
