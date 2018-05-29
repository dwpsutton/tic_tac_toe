from copy import deepcopy
from states import StateModel
from basic_response_model import basic_policy, random_action, possible_moves
from tic_tac_toe import isWinner


'''
Approach:
Need a way to recognise that an end state is a victory for player x or player y, these states 
should have a reward function of unity, all other zeros
Need a policy function that allows for a next move choice for each state, this can be deterministic
Need an
'''

GAMMA = 1.0


def get_team_from_state(board):
    num_x = len(filter(lambda x: x == 'X', board))
    num_o = len(filter(lambda x: x == 'O', board))
    if num_x > num_o:
        return 'O'
    elif num_x == num_o:
        return 'X'


def state_after_action(model, state, action):
    '''
    Returns state found by action
    :param model: The state model object
    :param state: The state where our action can be taken
    :param action: The action taken: tuple of (team string, move lever)
    :return: successor state after the action
    '''
    board = model.label_board_lookup[state]
    team = action[0]
    move = action[1]
    new_board = deepcopy(board)
    new_board[move] = team
    return model.board_labels_lookup[','.join(new_board)]


def evaluate(policy_function, reward_function, state_model):
    '''
    Evaluate value function for a given policy
    :param policy_function:
    :param reward_function:
    :param state_model:
    :return:
    '''
    # Initialise
    value_function = {}
    for s in range(state_model.num_labels):
        value_function[s] = 0.

    # evaluate
    tol = 1.E-6
    delta = 1E6
    while delta > tol:
        delta = 0.
        for s in range(state_model.num_labels):
            if isWinner(state_model.label_board_lookup[s], 'X') or isWinner(state_model.label_board_lookup[s], 'O'):
                # Game-end state: no rewards possible, leave value function zero
                continue
            action = policy_function[s]
            if action[1] is None:
                # No possible moves: game end state
                continue
            intermediate_state = state_after_action(state_model, s, action)
            v = deepcopy(value_function[s])
            value_function[s] = 0.
            for spr in state_model.transition_matrix[intermediate_state]:
                value_function[s] += state_model.transition_matrix[intermediate_state][spr] * \
                    (reward_function[intermediate_state][action[0]] + GAMMA * value_function[spr])
            delta = max(delta,abs(v-value_function[s]))
        print 'bing',delta
    return value_function


def main():
    # Create a state transition model
    state_model = StateModel(basic_policy)

    # Initialise
    reward_function = {}
    value_function = {}
    policy_function = {}
    for s in range(state_model.num_labels):
        board = state_model.label_board_lookup[s]
        policy_function[s] = (get_team_from_state(board), random_action(board))
        reward_function[s] = {'O': 1.0 if isWinner(board,'O') else 0.0,
                              'X': 1.0 if isWinner(board,'X') else 0.0
                              }
    value_function = evaluate(policy_function, reward_function, state_model)
#    print value_function
    print state_model.label_board_lookup[2926]
    print state_model.label_board_lookup[5949]
    print state_model.label_board_lookup[6019]
    xwin = [' ','X','X','X',' ','O',' ','O',' ',' ']
    s = state_model.board_labels_lookup[','.join(xwin)]
    print s, reward_function[s]['O'],reward_function[s]['X']
    print value_function[s]
    prev = [' ','X','X',' ',' ','O',' ','O',' ',' ']
    s = state_model.board_labels_lookup[','.join(prev)]
    print s, reward_function[s]['O'],reward_function[s]['X']
    print value_function[s]


if __name__ == "__main__":
    main()
