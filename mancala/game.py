import numpy as np


class Game:
    _default_board = np.array([4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0])

    def __init__(self, board=None, player_turn=None):
        self._board = Game._default_board[:] if board is None else board
        self._player_turn = True if player_turn is None else (player_turn == 1)

    def turn_player(self):
        """Check number of current player"""
        return 1 if self._player_turn else 2

    def board(self):
        """Current game board"""
        return self._board

    def print_board(self):
        """prints"""
        print(self._board)

    def __is_legal_move(self, index):
        """Checks if the given move is legal"""
        return self.__is_empty_hole(index) or self.__is_move_on_score_hole(index) or not self.__is_move_on_players_side(
            index)

    def __is_empty_hole(self, index):
        """Checks if given move is on an empty hole"""
        return self._board[index] == 0

    def __is_move_on_score_hole(self, index):
        """Checks if the given move is on a score hole"""
        return index == 6 or index == 13

    def __is_on_player_score_hole(self, index):
        """Checks if the given move is on the current players score hole"""
        if self._player_turn and index == 6:
            return True
        elif not self._player_turn and index == 13:
            return True

        return False

    def __is_move_on_players_side(self, index):
        """Checks if the move is on the current players side"""
        if self._player_turn:
            return 5 >= index >= 0
        else:
            return 12 >= index >= 7

    def score(self):
        return Game.score_boards(self._board)

    def winner(self):
        """Returns the winner player number, or 0 if the game isn't over"""
        if not Game.is_game_over(self._board):
            return 0
        return 1 if self.score()[0] > self.score()[1] else 2

    def move(self, index):
        """Perform a move action on a given index, based on the current player"""
        if Game.is_game_over(self._board):
            return self.score()

        if self.__is_legal_move(index):
            return self.score()

        steps = self._board[index]
        self._board[index] = 0
        curr_index = index

        while steps != 0:
            curr_index = (curr_index + 1) % len(self._board)
            if self.__is_move_on_score_hole(curr_index) and not self.__is_on_player_score_hole(curr_index):
                continue

            self._board[curr_index] += 1
            steps -= 1

        if self.__is_move_on_score_hole(curr_index) and not self.__is_on_player_score_hole(curr_index):
            """Move ends in players mancala can move again"""
            return self.score()

        """check if end move is on own side and on empty hole"""
        self.__capture_rule(curr_index)

        if Game.is_an_side_empty(self._board):
            self.__capture_all_stones_on_sides()

        self._player_turn = not self._player_turn
        return self.score()

    def clone(self):
        """Return a clone of the game object"""
        return Game(
            self.board(),
            self._player_turn()
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
            if self._player_turn:
                self._board[6] += captures
            else:
                self._board[13] += captures

    def __capture_all_stones_on_sides(self):
        self._board[6] += sum(self._board[0:6])
        self._board[13] += sum(self._board[7:13])
        self._board[0:6] = 0
        self._board[7:13] = 0

    @staticmethod
    def is_an_side_empty(board):
        return sum(board[0:6]) == 0 or sum(board[7:13]) == 0

    @staticmethod
    def score_boards(board):
        return board[6], board[13]

    @staticmethod
    def print_board(board):
        output = "\t" + str(board[0]) + " " + str(board[1]) + " " + str(board[2]) + " " + str(board[3]) + " " + str(
            board[4]) + " " + str(
            board[5]) + "\n"
        output += str(board[6]) + "\t\t\t\t " + str(board[13]) + "\n"
        output += "\t" + str(board[7]) + " " + str(board[8]) + " " + str(board[9]) + " " + str(board[10]) + " " + str(
            board[11]) + " " + str(board[12])

        print(output)

    @staticmethod
    def is_game_over(board):
        return Game.is_an_side_empty(board)
