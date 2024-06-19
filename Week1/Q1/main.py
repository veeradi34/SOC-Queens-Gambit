import json
import copy  # use it for deepcopy if needed
import math  # for math.inf
import logging

logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)

# Global variables in which you need to store player strategies (this is data structure that'll be used for evaluation)
# Mapping from histories (str) to probability distribution over actions
strategy_dict_x = {}
strategy_dict_o = {}


class History:
    def __init__(self, history=None):
        """
        # self.history : Eg: [0, 4, 2, 5]
            keeps track of sequence of actions played since the beginning of the game.
            Each action is an integer between 0-8 representing the square in which the move will be played as shown
            below.
              ___ ___ ____
             |_0_|_1_|_2_|
             |_3_|_4_|_5_|
             |_6_|_7_|_8_|

        # self.board
            empty squares are represented using '0' and occupied squares are either 'x' or 'o'.
            Eg: ['x', '0', 'x', '0', 'o', 'o', '0', '0', '0']
            for board
              ___ ___ ____
             |_x_|___|_x_|
             |___|_o_|_o_|
             |___|___|___|

        # self.player: 'x' or 'o'
            Player whose turn it is at the current history/board

        :param history: list keeps track of sequence of actions played since the beginning of the game.
        """
        if history is not None:
            self.history = history
            self.board = self.get_board()
        else:
            self.history = []
            self.board = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
        self.player = self.current_player()
        self.utility_playerx = 0

    def current_player(self):
        """ Player function
        Get player whose turn it is at the current history/board
        :return: 'x' or 'o' or None
        """
        total_num_moves = len(self.history)
        if total_num_moves < 9:
            if total_num_moves % 2 == 0:
                return 'x'
            else:
                return 'o'
        else:
            return None

    def get_board(self):
        """ Play out the current self.history and get the board corresponding to the history in self.board.

        :return: list Eg: ['x', '0', 'x', '0', 'o', 'o', '0', '0', '0']
        """
        board = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
        for i in range(len(self.history)):
            if i % 2 == 0:
                board[self.history[i]] = 'x'
            else:
                board[self.history[i]] = 'o'
        return board

    def is_win(self):
        # check if the board position is a win for either players
        # Feel free to implement this in anyway if needed
        if self.player == 'x':
            symbol = 'o'
        else:
            symbol = 'x'
        for i in range(0, 9, 3):
            if self.board[i] == symbol and self.board[i + 1] == symbol and self.board[i + 2] == symbol:
                return True
        for i in range(3):
            if self.board[i] == symbol and self.board[i + 3] == symbol and self.board[i + 6] == symbol:
                return True

        if self.board[0] == symbol and self.board[4] == symbol and self.board[8] == symbol:
            return True
        if self.board[2] == symbol and self.board[4] == symbol and self.board[6] == symbol:
            return True
        return False

    def is_draw(self):
        return '0' not in self.board and not self.is_win()

    def get_valid_actions(self):
        actions=[]
        for i in range(8):
            if self.board[i]=='0':
                actions.append(i)
        return actions
    def is_terminal_history(self):
        return self.is_win() or self.is_draw()

    def get_utility_given_terminal_history(self):
        if self.is_win():
            self.utility_playerx = 1 if self.player == 'o' else -1
        elif self.is_draw():
            self.utility_playerx = 0

    def update_history(self, action):
        new_history = self.history + [action]
        return History(new_history)


def backward_induction(history_obj):
    global strategy_dict_x, strategy_dict_o

    if history_obj.is_terminal_history():
        history_obj.get_utility_given_terminal_history()
        return history_obj.utility_playerx

    valid_moves = history_obj.get_valid_actions()
    current_player = history_obj.player
    best_utility = -math.inf if current_player == 'x' else math.inf
    best_action = None

    for move in valid_moves:
        new_history_obj = history_obj.update_history(move)
        utility = backward_induction(new_history_obj)

        if current_player == 'x':
            if utility > best_utility:
                best_utility = utility
                best_action = move
        else:
            if utility < best_utility:
                best_utility = utility
                best_action = move

    key = ''.join(map(str, history_obj.history))
    if current_player == 'x':
        strategy_dict_x[key] = {str(i): 1 if i == best_action else 0 for i in range(9)}
    else:
        strategy_dict_o[key] = {str(i): 1 if i == best_action else 0 for i in range(9)}

    history_obj.utility_playerx = best_utility if current_player == 'x' else -best_utility
    return history_obj.utility_playerx


def solve_tictactoe():
    backward_induction(History())
    with open('./policy_x.json', 'w') as f:
        json.dump(strategy_dict_x, f)
    with open('./policy_o.json', 'w') as f:
        json.dump(strategy_dict_o, f)
    print(strategy_dict_x)
    print(strategy_dict_o)


if __name__ == "__main__":
    logging.info("Start")
    solve_tictactoe()
    logging.info("End")
