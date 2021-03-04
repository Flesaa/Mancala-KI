import numpy as np
import mancalavars


class Mancala:
    _default_board = np.array([4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0])
    action_size = 12

    """
    The state of the game is a numpy array
    * Values are either 0 - 48
    * Shape [NUM_CHNLS, 14]
    0 - Batches
    2 - Turn (0 - Player 1, 1 - Player 2)
    3 - Invalid moves
    5 - Game over
    """

    def __init__(self, board=None, size=14):
        if board is None:
            self._board = np.zeros((mancalavars.NUM_CHNL, size))
            self._board[0] = self._default_board
        else:
            self._board = board

    def board(self):
        """Current game board"""
        return self._board

    def __is_legal_move(self, index):
        """Checks if the given move is legal"""
        return self.__is_empty_hole(index) or not self.__is_move_on_players_side(
            index)

    def __is_empty_hole(self, index):
        """Checks if given move is on an empty hole"""
        return self._board[index] == 0

    def __is_on_player_score_hole(self, index):
        """Checks if the given move is on the current players score hole"""
        if self.which_turn() and index == 6:
            return True
        elif not self.which_turn() and index == 13:
            return True

        return False

    def __is_move_on_players_side(self, index):
        """Checks if the move is on the current players side"""
        if self.which_turn():
            return 5 >= index >= 0
        else:
            return 12 >= index >= 7

    def winner(self):
        """Returns the winner player number, or 0 if the game isn't over"""
        if not self.is_game_over():
            return 0
        return 1 if self.score_boards()[0] > self.score_boards()[1] else 2

    def move(self, index):
        """Perform a move action on a given index, based on the current player"""
        if self.is_game_over():
            return self.score_boards()

        if self.__is_legal_move(index):
            return self.score_boards()

        steps = self._board[index]
        self._board[index] = 0
        curr_index = index

        while steps != 0:
            curr_index = (curr_index + 1) % len(self._board)
            if not self.__is_on_player_score_hole(curr_index):
                continue

            self._board[curr_index] += 1
            steps -= 1

        if not self.__is_on_player_score_hole(curr_index):
            """Move ends in players mancala can move again"""
            return self.score_boards()

        """check if end move is on own side and on empty hole"""
        self.__capture_rule(curr_index)

        if self.has_an_side_empty():
            self.__capture_all_stones_on_sides()

        self.switch_turn()

        return self.score_boards()

    def clone(self):
        """Return a clone of the game object"""
        return Mancala(
            self.board()
        )

    def __get_opposite_side_index(self, index):
        return (index + 7) % len(self._board)

    def __capture_rule(self, index):
        if self.__is_move_on_players_side(index) and self._board[index] == 1:
            """Capture opposite side"""
            opposite_side_index = self.__get_opposite_side_index(index)
            captures = 1 + self._board[opposite_side_index]
            self._board[index] = 0
            self._board[opposite_side_index] = 0
            if self.which_turn():
                self._board[6] += captures
            else:
                self._board[13] += captures

    def __capture_all_stones_on_sides(self):
        self._board[6] += sum(self._board[0:6])
        self._board[13] += sum(self._board[7:13])
        self._board[0:6] = 0
        self._board[7:13] = 0

    def has_an_side_empty(self):
        return sum(self._board[0:6]) == 0 or sum(self._board[7:13]) == 0

    def score_boards(self):
        return self._board[6], self._board[13]

    def str(self):
        board = "\t" + str(self._board[0]) + " " + str(self._board[1]) + " " + str(self._board[2]) + " " + str(
            self._board[3]) + " " + str(
            self._board[4]) + " " + str(
            self._board[5]) + "\n"
        board += str(self._board[6]) + "\t\t\t\t " + str(self._board[13]) + "\n"
        board += "\t" + str(self._board[7]) + " " + str(self._board[8]) + " " + str(self._board[9]) + " " + str(
            self._board[10]) + " " + str(
            self._board[11]) + " " + str(self._board[12])
        return board

    def is_game_over(self):
        return self.has_an_side_empty()

    def switch_turn(self):
        self._board[mancalavars.TURN_CHNL] = 1 - self._board[mancalavars.TURN_CHNL]

    def which_turn(self):
        return int(np.max(self._board[mancalavars.TURN_CHNL]))
