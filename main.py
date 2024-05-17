import pygame as pg
from game import Game

"""
    Runs the main loop of the game.
"""
if __name__ == '__main__':
    gameState = Game()
    gameState.main_loop()