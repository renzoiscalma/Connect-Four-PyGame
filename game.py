import pygame as pg
from constants import FPS
from ai import AI
from game_state import GameState
from enums import CellType
from copy import deepcopy

emptyState: list[list[CellType]] = [
  [CellType.EMPTY,CellType.EMPTY,CellType.EMPTY,CellType.EMPTY,CellType.EMPTY,CellType.EMPTY,CellType.EMPTY],
  [CellType.EMPTY,CellType.EMPTY,CellType.EMPTY,CellType.EMPTY,CellType.EMPTY,CellType.EMPTY,CellType.EMPTY],
  [CellType.EMPTY,CellType.EMPTY,CellType.EMPTY,CellType.EMPTY,CellType.EMPTY,CellType.EMPTY,CellType.EMPTY],
  [CellType.EMPTY,CellType.EMPTY,CellType.EMPTY,CellType.EMPTY,CellType.EMPTY,CellType.EMPTY,CellType.EMPTY],
  [CellType.EMPTY,CellType.EMPTY,CellType.EMPTY,CellType.EMPTY,CellType.EMPTY,CellType.EMPTY,CellType.EMPTY],
  [CellType.EMPTY,CellType.EMPTY,CellType.EMPTY,CellType.EMPTY,CellType.EMPTY,CellType.EMPTY,CellType.EMPTY],
]

class Game():
  def __init__(self):
    pg.init()
    self.clock = pg.time.Clock()
    self.screen = pg.display.set_mode((1280, 768))
    self.running = True
    self.gameState = GameState(deepcopy(emptyState))
    self.xOffset = 165
    self.yOffset = 200
    self.colGap = 80
    self.rowGap = 80
    self.current_turn = CellType.PLAYER_1
    self.move = -1
    self.won = -1
    self.font = pg.font.SysFont('Comic Sans MS', 30)
    self.ai = AI(self.gameState, CellType.PLAYER_2)

  def main_loop(self):
    while self.running:
      self.events_handler()
      self.update()
      self.screen.fill("black")
      self.draw()
      pg.display.flip()
      # limits FPS to 60 
      # dt is delta time in seconds since last frame, used for framerate-
      # independent physics.
      self.dt = self.clock.tick(FPS) / 1000
    pg.quit()

  def events_handler(self):
    for event in pg.event.get():
        if event.type == pg.QUIT:
          self.running = False
        if (self.current_turn == CellType.PLAYER_1 and 
            event.type == pg.KEYUP and 
            self.won < 0 and 
            pg.K_0 < event.key <= pg.K_7):
          self.move = event.key - pg.K_1
        if (event.type == pg.KEYUP and 
            self.won >= 0 and
            event.key == pg.K_r):
          self.reset()
    pass

  def update(self):
    if self.won > 0:
      return
    if self.move != -1 and self.current_turn == CellType.PLAYER_1:
      if (self.gameState.player_move(self.current_turn, self.move)):
        self.won = self.gameState.player_won()
        # print(self.won)
        self.turn_change()
        print("player 1 score: ", self.gameState.get_score(CellType.PLAYER_1))
      self.move = -1
    elif (self.current_turn == CellType.PLAYER_2):
      turn_finished = False
      while (not turn_finished):
        turn_finished = self.gameState.player_move(self.current_turn, self.ai.make_turn(self.gameState))
        self.won = self.gameState.player_won()
        self.turn_change()
      self.move = -1


  def draw(self):
    self.draw_board()
    self.draw_text()
    pass
  
  def turn_change(self):
    if self.current_turn == CellType.PLAYER_1:
      self.current_turn = CellType.PLAYER_2
    else:
      self.current_turn = CellType.PLAYER_1

  def draw_board(self):
    for rowIdx, row in enumerate(self.gameState.board):
      for colIdx, cell in enumerate(row):
        circle_posX = self.xOffset + (self.colGap * (colIdx + 1))
        circle_posY = self.yOffset + (self.rowGap * (rowIdx + 1))
        if cell == CellType.PLAYER_1:
          pg.draw.circle(self.screen, "red", pg.Vector2(circle_posX, circle_posY), 30)
        elif cell == CellType.PLAYER_2:
          pg.draw.circle(self.screen, "blue", pg.Vector2(circle_posX, circle_posY), 30)

  def draw_text(self):
    if self.won == -1:
      txt_color = (255, 0, 0) if self.current_turn == CellType.PLAYER_1 else (0, 0, 255) 
      txt = self.font.render("Player {}'s Turn".format(self.current_turn.value), True, txt_color)
    elif self.won == CellType.PLAYER_1.value:
      txt_color = (255, 0, 0)
      txt = self.font.render("Player 1 Won!", True, txt_color)
    elif self.won == CellType.PLAYER_2.value:
      txt_color = (0, 0, 255)
      txt = self.font.render("Player 2 Won!", True, txt_color)
    else:
      txt_color = (0, 255, 255)
      txt = self.font.render("Draw!", True, txt_color)
    txt_x = self.screen.get_width() / 2 - txt.get_rect().width / 2
    txt_y = 0
    self.screen.blit(txt, (txt_x, txt_y))
    for i in range(1, self.gameState.num_cols + 1):
      txt = self.font.render(str(i), True, (255, 255, 255))
      txt_x = 158 + (80 * (i))
      txt_y = 768 - 60
      self.screen.blit(txt, (txt_x, txt_y))
    
    txt = self.font.render("Press 1-7 to choose a column.", True, (255, 255, 255))
    txt_x = 158 + (80 * (self.gameState.num_cols + 1))
    txt_y = 768 - 60
    self.screen.blit(txt, (txt_x, txt_y))

  
  def reset(self):
    self.gameState = GameState(deepcopy(emptyState))
    self.current_turn = CellType.PLAYER_1
    self.move = -1
    self.won = -1
