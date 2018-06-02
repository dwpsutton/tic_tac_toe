from copy import deepcopy
from numpy.random import shuffle
from states import StateModel
from basic_response_model import basic_policy, random_action, possible_moves
from tic_tac_toe import isWinner, drawBoard


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


def expected_action_value(s, action, value_function, reward_function, state_model):
    '''
    Compute expectation of value function of successor state given current action
    :param s:
    :param action:
    :param value_function:
    :param reward_function:
    :param state_model:
    :return: expected action value
    '''
    intermediate_state = state_after_action(state_model, s, action)
    action_value = 0.
    for spr in state_model.transition_matrix[intermediate_state]:
        action_value += state_model.transition_matrix[intermediate_state][spr] * \
                        (reward_function[intermediate_state][action[0]] + GAMMA * value_function[spr])
    return action_value


def evaluate(policy_function, reward_function, state_model):
    '''
    Evaluate value function for a given policy
    :param policy_function:
    :param reward_function:
    :param state_model:
    :return: value function
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
            if action is None:
                print 'yo', s
                print policy_function
            if action[1] is None:
                # No possible moves: game end state
                continue
            v = deepcopy(value_function[s])
            value_function[s] = expected_action_value(s, action, value_function, reward_function, state_model)
            delta = max(delta, abs(v-value_function[s]))
        # print 'bing',delta
    return value_function


def improve(value_function, reward_function, state_model):
    '''
    Return the optimal policy function for a given value function
    :param value_function:
    :param reward_function:
    :param state_model:
    :return: optimal policy function
    '''
    policy_function = {}
    for s in range(state_model.num_labels):
        board = state_model.label_board_lookup[s]
        moves = possible_moves(board)
        best_action_value = 0.
        best_action = (get_team_from_state(board), None)
        if moves is not None:
            # shuffle moves here to pick random if many optimal moves, except policy iteration won't converge
            for m in moves:
                action = (best_action[0], m)
                action_value = expected_action_value(s, action, value_function, reward_function, state_model)
                if action_value > best_action_value:
                    best_action = action
        policy_function[s] = best_action
    return policy_function


def policy_stable(old_policy_function, new_policy_function):
    '''
    Return True if the policy functions are identical
    :param old_policy_function:
    :param new_policy_function:
    :return: Boolean
    '''
    for s in range(len(old_policy_function)):
        if old_policy_function[s] != new_policy_function[s]:
            return False
    return True


def policy_iteration(state_model):
    # Initialise
    reward_function = {}
    policy_function = {}
    for s in range(state_model.num_labels):
        board = state_model.label_board_lookup[s]
        policy_function[s] = (get_team_from_state(board), random_action(board))
        reward_function[s] = {'O': 1.0 if isWinner(board,'O') else 0.0,
                              'X': 1.0 if isWinner(board,'X') else 0.0
                              }

    converged = False
    ctr = 0
    while not converged:
        value_function = evaluate(policy_function, reward_function, state_model)
        new_policy_function = improve(value_function, reward_function, state_model)
        converged = policy_stable(policy_function, new_policy_function)
        policy_function = new_policy_function
        ctr += 1
        print 'Iteration :', ctr
    return policy_function, value_function


def main():
    # Create a state transition model
    state_model = StateModel(basic_policy)

    # Initialise
    reward_function = {}
    policy_function = {}
    for s in range(state_model.num_labels):
        board = state_model.label_board_lookup[s]
        policy_function[s] = (get_team_from_state(board), random_action(board))
        reward_function[s] = {'O': 1.0 if isWinner(board,'O') else 0.0,
                              'X': 1.0 if isWinner(board,'X') else 0.0
                              }
    value_function = evaluate(policy_function, reward_function, state_model)
    xwin = [' ','X','X','X',' ','O',' ','O',' ',' ']
    drawBoard(xwin)
    s = state_model.board_labels_lookup[','.join(xwin)]
    print s, reward_function[s]['O'],reward_function[s]['X']
    print value_function[s]
    prev = [' ','X','X',' ',' ','O',' ','O',' ',' ']
    drawBoard(prev)
    s = state_model.board_labels_lookup[','.join(prev)]
    print s, reward_function[s]['O'],reward_function[s]['X']
    print value_function[s], policy_function[s]

    print 'Now trying:'
    policy_function, value_function = policy_iteration(state_model)

    print 'Quick test'
    prev = [' ','X','X',' ',' ','O',' ','O',' ',' ']
    drawBoard(prev)
    s = state_model.board_labels_lookup[','.join(prev)]
    print s, reward_function[s]['O'],reward_function[s]['X']
    print value_function[s], policy_function[s]

    early = [' ','X',' ',' ',' ','O',' ',' ',' ',' ']
    drawBoard(early)
    s = state_model.board_labels_lookup[','.join(early)]
    print value_function[s], policy_function[s]

    empty = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
    drawBoard(empty)
    print get_team_from_state(empty)
    s = state_model.board_labels_lookup[','.join(empty)]
    print state_model.num_labels
    print value_function[s], policy_function[s]


if __name__ == "__main__":
    main()
