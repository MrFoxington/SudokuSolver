import boards
import solver

# print('testing')
# s = solver.Solver()
# s.load_puzzle(boards.board_easy)
# print('done')


def sayHi(count):
    print('HI CUTIE!!!')
    if count >= 0:
        sayHi(count-1)


sayHi(10)