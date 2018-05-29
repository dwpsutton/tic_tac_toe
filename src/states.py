'''
Want a converter from board to state label
Want a list of transitions between each state label its possible successors
A response model will be a probability assigned to each transition
'''

from copy import deepcopy
from basic_response_model import basic_policy as initial_response_model
from tic_tac_toe import isSpaceFree

class StateModel(object):
    def __init__(self, response_model):
        self.MAX_GRID_SIZE = 10
        self.response_model = response_model
        self.num_labels = -1
        self.board_labels_lookup = {}
        self.label_board_lookup = {}
        self.transition_matrix = {}
        self.label_boards([' ' for i in range(self.MAX_GRID_SIZE)], 1)
        self.build_transition_matrix()

    def build_transition_matrix(self):
        '''
        for each state, add a dict of transitions with probabilities
        :return:
        '''
        for s in range(len(self.board_labels_lookup)):
            self.transition_matrix[s] = {}
            board = self.label_board_lookup[s]
            num_x = len(filter(lambda x: x == 'X', board))
            num_o = len(filter(lambda x: x == 'O', board))
            if num_x > num_o:
                computer_letter = 'O'
            elif num_x == num_o:
                computer_letter = 'X'
            else:
                raise(ValueError,str.format("num_x must equal num_o or num_o+1, saw num_x={} num_o={}", num_x, num_o))
            move_probabilities = self.response_model(board, computer_letter)
            if move_probabilities is None:
                continue
            moves = filter(lambda i: move_probabilities[i] > 0., range(self.MAX_GRID_SIZE))
            if len(moves) >= 1:
                for move in moves:
                    new_board = deepcopy(board)
                    new_board[move] = computer_letter
                    new_s = self.board_labels_lookup[','.join(new_board)]
                    self.transition_matrix[s][new_s] = move_probabilities[move]
        return None

    def label_boards(self, board, pos):
        if pos == self.MAX_GRID_SIZE:
            # Completed state
            if check_legal(board):
                self.num_labels += 1
                this_label = deepcopy(self.num_labels)
                self.label_board_lookup[this_label] = deepcopy(board)
                self.board_labels_lookup[','.join(board)] = this_label
                return 1
            else:
                return 0
        elif pos < 1:
            return self.label_boards(board, 1)
        else:
            # Explore next position's three possible states
            counter = 0
            board[pos] = 'X'
            counter += self.label_boards(board, pos+1)
            board[pos] = 'O'
            counter += self.label_boards(board, pos+1)
            board[pos] = ' '
            counter += self.label_boards(board, pos+1)
            return counter


def check_legal(board):
    num_x = len(filter(lambda x: x == 'X', board))
    num_o = len(filter(lambda x: x == 'O', board))
    return (num_x == num_o) or (num_x == num_o + 1)


def run_tests():
    mymodel = StateModel(initial_response_model)
    print len(mymodel.board_labels_lookup)
    print 'Test 1:'
    board = [' ',
             'X', ' ', 'O',
             ' ', 'X', ' ',
             'O', ' ', ' ']
    print board[1:4]
    print board[4:7]
    print board[7:10]
    for k, v in mymodel.transition_matrix[mymodel.board_labels_lookup[','.join(board)]].iteritems():
        board = mymodel.label_board_lookup[k]
        print 'prob = ', v
        print board[1:4]
        print board[4:7]
        print board[7:10]
    print 'Test 2:'
    board = [' ',
             ' ', ' ', ' ',
             ' ', 'X', ' ',
             'O', ' ', ' ']
    print board[1:4]
    print board[4:7]
    print board[7:10]
    for k, v in mymodel.transition_matrix[mymodel.board_labels_lookup[','.join(board)]].iteritems():
        board = mymodel.label_board_lookup[k]
        print 'prob = ', v
        print board[1:4]
        print board[4:7]
        print board[7:10]

if __name__ == "__main__":
    run_tests()