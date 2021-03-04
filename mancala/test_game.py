from unittest import TestCase
import numpy as np
from mancala.game import Game


class TestGame(TestCase):

    def test_is_game_over_invalid(self):
        game = Game()
        self.assertFalse(game.is_game_over())

    def test_is_game_over_invalid(self):
        board = np.array([0, 0, 0, 0, 0, 0, 24, 4, 4, 4, 4, 4, 4, 0])

        game = Game(board=board)

        self.assertTrue(game.is_game_over())

        board = np.array([4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 24])
        game = Game(board=board)

        self.assertTrue(game.is_game_over())

    def test_move_capture(self):
        board = np.array([0, 0, 0, 3, 0, 8, 15, 4, 4, 4, 4, 4, 4, 0])

        game = Game(board=board)
        game.move(5)
        Game.print_board(game.board())
        self.assertEqual(game.score()[0], 22)

        board = np.array([13, 0, 0, 0, 0, 0, 15, 4, 4, 4, 4, 4, 4, 0])
        game = Game(board=board)
        game.move(0)
        Game.print_board(game.board())
        self.assertEqual(game.score()[0], 22)
        self.assertEqual(game.board()[0], 0)
        self.assertEqual(game.board()[7], 0)
        self.assertEqual(game.board()[8], 5)

        board = np.array([0, 0, 0, 0, 0, 8, 15, 4, 4, 4, 4, 4, 4, 0])
        game = Game(board=board)
        game.move(5)
        Game.print_board(game.board())
        self.assertEqual(game.score()[0], 22)
        self.assertEqual(game.score()[1], 25)
