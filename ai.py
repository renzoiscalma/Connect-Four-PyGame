import random
import math
from game_state import GameState
from enums import CellType
from copy import deepcopy

class AI():
  def __init__(self, board_state: GameState, player):
    self.player = player
    self.opposing = CellType.PLAYER_1 if player == CellType.PLAYER_2 else CellType.PLAYER_2

  def make_turn(self, board_state):
    value, best_move = self.minimax(board_state, 3, self.player)
    print("v:", value)
    print("ai best move: ", best_move)
    return best_move
  
  """
    returns tuple, value and move
  """
  def minimax(self, node: GameState, depth, player_max):
    player_won = node.player_won()
    terminal_node = player_won != -1
    if depth == 0: # stalemate, terminal node
      return node.get_score(self.player), -1
    if terminal_node:
      if player_won == self.player.value:
        return math.inf, -1
      elif player_won == self.opposing.value:
        return -math.inf, -1
      elif player_won == 0:
        return 0, -1
    if player_max == self.player:
      best_value = -math.inf
      best_move = -1
      scores = [0] * 7
      for colIdx, col_stack_size in enumerate(node.board_stack_size):
        if (col_stack_size < node.num_rows):
          gameStateCopy = GameState(deepcopy(node.board)) # deep copy to avoid mutating the original state
          gameStateCopy.player_move(self.player, colIdx)
          value = self.minimax(gameStateCopy, depth - 1, self.opposing)[0]
          scores[colIdx] = value
          if value >= best_value:
            best_value = value
            best_move = colIdx
      return best_value, best_move
    else:
      best_value = math.inf
      best_move = -1
      scores = [0] * 7
      for colIdx, col_stack_size in enumerate(node.board_stack_size):
        if (col_stack_size < node.num_rows):
          gameStateCopy = GameState(deepcopy(node.board)) # deep copy to avoid mutating the original state
          gameStateCopy.player_move(self.opposing, colIdx)
          value = self.minimax(gameStateCopy, depth - 1, self.player)[0]
          scores[colIdx] = value
          if value <= best_value:
            best_value = value
            best_move = colIdx
      return best_value, best_move
