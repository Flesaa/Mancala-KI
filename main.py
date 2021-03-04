# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np

from gym_mancala.envs import MancalaEnv


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    env = MancalaEnv()
    while not MancalaEnv.is_game_over(env.board()):
        env.print_board(env.board())
        print("Choose next move player {player}".format(player=1+ int(env.turn_player() is True)))
        move = int(input())
        env.move(move - 1)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
