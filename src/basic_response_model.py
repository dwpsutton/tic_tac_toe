import tic_tac_toe
import numpy.random as random

def basic_policy(board, computerLetter):
    '''
    Given a board and the computer's letter, return a probability distribution for the next move
    '''
    if computerLetter == 'X':
        playerLetter = 'O'
    else:
        playerLetter = 'X'

    response_probabilities = [0.0 for i in range(10)]

    # Here is our algorithm for our Tic Tac Toe AI:
    # First, check if we can win in the next move
    for i in range(1, 10):
        copy = tic_tac_toe.getBoardCopy(board)
        if tic_tac_toe.isSpaceFree(copy, i):
            tic_tac_toe.makeMove(copy, computerLetter, i)
            if tic_tac_toe.isWinner(copy, computerLetter):
                response_probabilities[i]= 1.0
                return response_probabilities

    # Check if the player could win on his next move, and block them.
    for i in range(1, 10):
        copy = tic_tac_toe.getBoardCopy(board)
        if tic_tac_toe.isSpaceFree(copy, i):
            tic_tac_toe.makeMove(copy, playerLetter, i)
            if tic_tac_toe.isWinner(copy, playerLetter):
                response_probabilities[i]= 1.0
                return response_probabilities

    # Try to take one of the corners, if they are free.
    movesList = [1, 3, 7, 9]
    for i in movesList:
        if tic_tac_toe.isSpaceFree(board, i):
            response_probabilities[i] = 1.0
    if sum(response_probabilities) > 0.1:
        return [x / sum(response_probabilities) for x in response_probabilities]

    # Try to take the center, if it is free.
    if tic_tac_toe.isSpaceFree(board, 5):
        response_probabilities[5] = 1.0
        return response_probabilities

    # Move on one of the sides.
    movesList = [2, 4, 6, 8]
    for i in movesList:
        if tic_tac_toe.isSpaceFree(board, i):
            response_probabilities[i] = 1.0
    if sum(response_probabilities) > 0.1:
        return [x / sum(response_probabilities) for x in response_probabilities]


def basic_policy_action(board, computer_letter):
    '''Given a board and a side, choose an action from the basic policy'''
    move_probability_distr = basic_policy(board, computer_letter)
    return random.choice(range(10), p=move_probability_distr)


def possible_moves(board):
    '''Given a board, return iterable of possible moves'''
    available_moves = []
    for i in range(1, 10):
        if tic_tac_toe.isSpaceFree(board, i):
            available_moves.append(i)
    return available_moves


def random_action(board):
    '''Given a board, choose a random legal move'''
    available_moves = possible_moves(board)
    if len(available_moves) > 0:
        return random.choice(available_moves)
    else:
        return None
