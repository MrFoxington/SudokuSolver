import boards
import solver

print('testing')
s = solver.Solver()
s.load_puzzle(boards.board_evil2)
s.solve()
print('Done')
