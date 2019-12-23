App (Top Level To run and Init project)
    - Read Input for sudoku data
    - Generate sudoku data object
    - Pass/Run Solver using generated sudoku puzzle

Solver (Obvious Class designed to solve sudoku)
    - Scan through puzzle and determin potential options for every square
    - Locate squares with only 1 possibility
        - Fill in square with single possibility
        - Update all possibilities of affected squares (Row,Column,Sector)
    - IF unable to locate 1 posibility square, run backtracking algorithm to determine best possible options for lowest option squares
        - LEARN HOW TO IMPLEMENT A BACKTRACKING ALGORITHM!
    - Repeat

Sudoku
    - 2d Array to store values (Row,Col)
        - Potential 3d Array to store more data for each square (done)
        - Move into Solver class? (Not pure data handling, is solving/solution data?)
            - Store Potential Values (Values that are valid to be entered into square)
            - Store Guess Values (User enters their potential guesses to be stored)
    - Determine sector managment (9 sectors, 1/3 of each row/col) (done)
    - Validate value
        - Check if added/selected value is valid for location
        - Check if valid without adding to array?? (maybe)
    - Validate puzzle (done)
        - Check if puzzle is valid in current state
        - Iterate over each square with Validate Value



Backtracking Algorithm

function solve( board )
    if the board contains no invalid cells, ie.cells that violate the rules:
        if it is also completely filled out then
            return true
    for each cell in the board
        if the cell is empty
            for each number in {1,2,3}
                replace the current cell with number
                if solve(board) and the board is valid
                    return true
                else
                    backtrack
        return false