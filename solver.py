import copy
import sudoku
import boards


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
        guesses = range(1, 10)
        guesses = [x for x in guesses if x not in puzzle.get_row(row)]
        guesses = [x for x in guesses if x not in puzzle.get_col(col)]
        guesses = [x for x in guesses if x not in puzzle.get_box(row, col)]
        return guesses

    # Oh god, send help!. This is turning into a clusterfuck...
    def update_guesses_by_cell(self, guesses, puzzle, row, col):
         # Get all other cells affected by updated Cell
         # Itterate through cells and remove value from guesses from
        pass

    # TODO: Learn Backtracking algorithm
    def solve(self):
        empty = 0
        for row in self.puzzle.board:
            empty += row.count(0)

        self.__solve_dumb(self.puzzle, empty)

    # Smart Recursive Solver (locates lowest guess count)
    def __solve(self, puzzle, guesses, empty):
        print('Solving!')
        if empty <= 0:
            if puzzle.validate_board():
                print(puzzle)
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
            tmp_guesses = copy.deepcopy(self.update_guesses_by_cell(guesses, tmp_puzzle, row, col))
            tmp_guesses[row][col] = []
            if self.__solve(tmp_puzzle, tmp_guesses, empty - 1):
                puzzle = tmp_puzzle
                guesses = tmp_guesses
                return True
            else:
                tmp_puzzle.board[row][col] = 0
        return False

    # Find cell with least options (Guess count)
    def __find_best_cell_row_col(self, guesses):
        # [Guess Count, row, col)
        best_cell = None
        for x, row in enumerate(guesses):
            for y, cell in enumerate(row):
                if len(cell) > 0:
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
s.load_puzzle(boards.board_easy)
s.solve()
print("Done Run!")
