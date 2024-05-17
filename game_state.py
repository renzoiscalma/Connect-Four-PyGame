from enums import CellType

class GameState():
  def __init__(self, board_state: list[list[CellType]]):
    self.board = board_state
    self.num_cols = len(board_state[0])
    self.num_rows = len(board_state)
    self.board_stack_size: list = [0] * self.num_cols
    for col in range(self.num_cols): # calculate stack size for each columns
      self.board_stack_size[col] = sum(1 for row in self.board if row[col] != CellType.EMPTY)
  
  def player_move(self, cell_type: CellType, col: int):
    stack_size = self.board_stack_size[col]
    if stack_size >= self.num_rows:
      return False
    else:
      self.board[self.num_rows - stack_size - 1][col] = cell_type
      self.board_stack_size[col] += 1
      return True
  
  """
    for each cell, check horizontally, vertically and diagonally if there's a 4 connect
    returns 
    -1, if not over
    0 draw
    1 player 1 won
    2 player 2 won
  """
  def player_won(self):
    for rowIdx, row in enumerate(self.board):
      for colIdx, col in enumerate(row):
        if col == CellType.EMPTY:
          continue
        # horizontal check
        try:
          if (self.board[rowIdx][colIdx] == 
              self.board[rowIdx+1][colIdx] == 
              self.board[rowIdx+2][colIdx] == 
              self.board[rowIdx+3][colIdx]):
            return self.board[rowIdx][colIdx].value
        except IndexError:
          pass
        
        # vertical check
        try:
          if (self.board[rowIdx][colIdx] == 
              self.board[rowIdx][colIdx+1] == 
              self.board[rowIdx][colIdx+2] == 
              self.board[rowIdx][colIdx+3]):
            return self.board[rowIdx][colIdx].value
        except  IndexError:
          pass

        # low right - diagonal check
        try:
          if (not colIdx + 3 < 0 and 
              self.board[rowIdx][colIdx] ==                                      
              self.board[rowIdx + 1][colIdx + 1] ==                                      
              self.board[rowIdx + 2][colIdx + 2] ==                                      
              self.board[rowIdx + 3][colIdx + 3]):
            return self.board[rowIdx][colIdx].value
        except IndexError:
          pass

        # up right - diagonal check
        try:
          if (not colIdx - 3 < 0 and 
              self.board[rowIdx][colIdx] == 
              self.board[rowIdx + 1][colIdx - 1] == 
              self.board[rowIdx + 2][colIdx - 2] == 
              self.board[rowIdx + 3][colIdx - 3]):
            return self.board[rowIdx][colIdx].value
        except IndexError:
          pass
        
    total_pieces = sum(self.board_stack_size)
    # print("Total pieces: " + str(total_pieces))
    if total_pieces == self.num_cols * self.num_rows:
      return 0
    
    return -1

      
  def get_score(self, player: CellType):
    score = 0
    opposing_player = CellType.PLAYER_1 if player == CellType.PLAYER_2 else CellType.PLAYER_2
    for i in range(self.num_rows):
      for j in range(self.num_cols):
        score += self.check_vertical_streaks(i, j, player, opposing_player)
        score += self.check_horizontal_streaks(i, j, player, opposing_player)
        score += self.check_positive_diagonal_streaks(i, j, player, opposing_player)
        score += self.check_negative_diagonal_streaks(i, j, player, opposing_player)
    return score
  
  def check_negative_diagonal_streaks(self, i, j, player, opposing_player):
    cell_score = 0
    for length in range(2, 5):
      if i + length < self.num_rows and j - length >= 0:
        streak = [self.board[i+k][j-k] for k in range(length)]
        cell_score += self.get_streak_score(streak, player, opposing_player)
    return cell_score
  
  def check_positive_diagonal_streaks(self, i, j, player, opposing_player):
    cell_score = 0
    for length in range(2, 5):
      if i + length < self.num_rows and j + length <= self.num_cols:
        streak = [self.board[i+k][j+k] for k in range(length)]
        cell_score += self.get_streak_score(streak, player, opposing_player)
    return cell_score

  def check_vertical_streaks(self, i, j, player, opposing_player):
    cell_score = 0
    for length in range(2, 5):
      if i + length < self.num_rows:
        streak = [self.board[i+k][j] for k in range(length)]
        cell_score += self.get_streak_score(streak, player, opposing_player)
    return cell_score

  def check_horizontal_streaks(self, i, j, player, opposing_player):
    cell_score = 0
    for length in range(2, 5):
      if j + length < self.num_cols:
        streak = self.board[i][j:j+length]
        cell_score += self.get_streak_score(streak, player, opposing_player)
    return cell_score
  
  def get_streak_score(self, streak_list, player, opposing_player):
    if all(cell == player for cell in streak_list):
      return 10 ** (len(streak_list))     # 10^streak - 1 length is the score for this cell
    if all(cell == opposing_player for cell in streak_list):
      return -(10 ** (len(streak_list)))  # -10^streak - 1
    return 0