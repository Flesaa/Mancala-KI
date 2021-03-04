import numpy as np
import gym
from gym import error, spaces, utils
from gym.utils import seeding

from gym_mancala import mancalavars
from gym_mancala.Mancala import Mancala


class MancalaEnv(gym.Env):
    metadata = {'render.modes': ['terminal']}



    def __init__(self, board=None):
        self._board = board
        self.mancala = Mancala(board=board)
        self._state = np.copy(self.mancala.board())
        self.observation_space = gym.spaces.Box(np.float32(0), np.float32(mancalavars.NUM_CHNL), shape=(mancalavars.NUM_CHNL, len(board)))
        self.action_space = gym.spaces.Discrete(Mancala.action_size)
        self.done = False

    def step(self, action):
        assert not self.done
        self.mancala.move(action)
        self._state = self.mancala.board()
        self.done = self.mancala.is_game_over()
        return np.copy(self._state), self.mancala.score_boards()[0], self.done

    def reset(self):
        self.mancala = Mancala(self._board)
        self._state = self.mancala.board()
        self.done = False
        return np.copy(self._state)

    def render(self, mode='terminal'):
        if mode == 'terminal':
            print(self.mancala.str())
