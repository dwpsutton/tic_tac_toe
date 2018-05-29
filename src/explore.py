
'''
Start with top left (1).
For each state of (1), try a different state of (2)
Recursively do this until all state filled in.
Increment count, when the final state is legal sum(X) == sum(0) or sum(O) == sum(O) + 1
'''

MAX_GRID_SIZE = 10


def check_legal(board):
    num_x = len(filter(lambda x: x == 'X', board))
    num_o = len(filter(lambda x: x == 'O', board))
    return (num_x == num_o) or (num_x == num_o + 1)


def try_state(board, pos):
    if pos == MAX_GRID_SIZE:
        # Completed state
        if check_legal(board):
            return 1
        else:
            return 0
    else:
        # Explore next position's three possible states
        counter = 0
        board[pos] = 'X'
        counter += try_state(board, pos+1)
        board[pos] = 'O'
        counter += try_state(board, pos+1)
        board[pos] = ' '
        counter += try_state(board, pos+1)
        return counter


if __name__ == "__main__":
    game_board = [' ' for i in range(MAX_GRID_SIZE)]
    print try_state(game_board, 1)
