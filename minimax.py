import numpy as np
import copy

# ===== What can this class do? =====
# From a state we can:
#   - Check if it is terminal
#   - Get its children
#   - Get it value (if it is terminal), get it minimax value (if not terminal)
# This class need to have
#   - A matrix represent the board game
#   - Which player just_played, which player is next_to_play

# 'O' is maxplayer, 'X' is the minplayer
class State:
    def __init__(self, just_played, next_to_play, matrix=None) -> None:
        if matrix is None:
            self.matrix = np.full((3, 3), ' ')
        else:
            self.matrix = matrix
        self.just_played = just_played
        self.next_to_play = next_to_play

    def is_win(self):
        # Row
        for i in range(3):
            if self.matrix[i, 0] == self.matrix[i, 1] == self.matrix[i, 2] == self.just_played:
                return True
        # Col
        for i in range(3):
            if self.matrix[0, i] == self.matrix[1, i] == self.matrix[2, i] == self.just_played:
                return True
        # Dia
        if self.matrix[0, 0] == self.matrix[1, 1] == self.matrix[2, 2] == self.just_played:
            return True
        if self.matrix[2, 0] == self.matrix[1, 1] == self.matrix[0, 2] == self.just_played:
            return True

    def is_draw(self):
        if not self.is_win():
            for i in range(3):
                for j in range(3):
                    if self.matrix[i, j] == ' ':
                        return False
            return True

    def get_value(self):
        if self.is_win():
            if self.just_played == 'X':
                return -10
            if self.just_played == 'O':
                return 10
        elif self.is_draw():
            return 0

        # We dont care about non-terminal case

    def get_children(self):
        # If the state is terminal state there is no need to find children
        if self.is_win() or self.is_draw():
            return None

        # Get all children, dont care for duplicate by mirror
        children = []
        for i in range(3):
            for j in range(3):
                if self.matrix[i, j] == ' ':
                    new_matrix = copy.deepcopy(self.matrix)
                    new_matrix[i, j] = self.next_to_play
                    children.append(
                        State(just_played=self.next_to_play, next_to_play=self.just_played, matrix=new_matrix))
        return children

    def minimax(self):
        if self.is_win() or self.is_draw():
            return self.get_value()

        # Last turn X play, this time O play (Maxplayer)
        if self.just_played == 'X':
            n_max = -1e9
            children = self.get_children()
            for child in children:
                score = child.minimax()
                n_max = max(n_max, score)
            return n_max

        # Last turn O play, this time X play (Minplayer)
        if self.just_played == 'O':
            n_min = 1e9
            children = self.get_children()
            for child in children:
                score = child.minimax()
                n_min = min(n_min, score)
            return n_min


matrix = np.array([['X', 'X', 'O'],
                   ['X', 'O', 'X'],
                   [' ', 'O', 'O']])
state = State('O', 'X', matrix)
children = state.get_children()
for child in children[1:]:
    print(child.matrix)