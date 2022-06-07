from random import sample
import numpy as np
from cell import Cell
from reprinter import Reprinter

rep = Reprinter()

class Game:
  rows = None
  cols = None
  mines = None
  board = None
  started = False

  def __init__(self, rows, cols, mines):
    self.rows = rows
    self.cols = cols
    self.mines = mines
    shape = (self.rows, self.cols)
    self.board = np.ndarray(shape, dtype=np.dtype(Cell))
    for i in range(self.rows):
      for j in range(self.cols):
        self.board[i][j] = Cell()

  def checkWinLose(self):
    win = True
    lose = False
    for i in range(self.rows):
      for j in range(self.cols):
        c = self.getCell([i, j])
        if c.mine and not c.hidden:
          return (False, True)
        if c.hidden and not c.flag:
          win = False
    return (win, lose)

  def printBoard(self, reveal=False, highlightPos=[]):

    win, lose = self.checkWinLose()

    if win or lose:
      reveal = True

    minesLeft = self.mines
    for i in range(self.rows):
      for j in range(self.cols):
        cell = self.getCell([i, j])
        if cell.flag:
          minesLeft -= 1
    toPrint = "Mines left: " + str(minesLeft) + "\n|" + "--" * self.cols + "|\n|"
    for i in range(self.rows):
      for j in range(self.cols):
        cell = self.board[i][j]
        value = cell.toString(reveal)
        highlight = [i, j] == highlightPos
        prefix = "\033[1m\033[34m" if highlight else ""
        postfix = "\033[0m" if highlight else ""
        value = value if (value.strip() or not highlight) else "+"
        toPrint += f" {prefix}{value}{postfix}"
      toPrint += "|\n|"
    toPrint += "--" * self.cols + "|\n"

    if win:
      toPrint += "You won!\n"
    elif lose:
      toPrint += "You lost!\n"
    else:
      toPrint += "Arrow keys to move | Space to reveal | F to flag | S to solve\n"

    rep.reprint(toPrint)
    if win or lose:
      exit()

  def getCell(self, p):
    return self.board[p[0]][p[1]]

  def getNeighbours(self, i, j):
    result = []
    neighbors = [[i-1,j],[i-1,j+1],[i,j-1],[i+1,j-1],[i+1,j],[i+1,j+1],[i,j+1],[i-1,j-1]]
    for n in neighbors:
      if 0 <= n[0] <= self.rows-1 and 0 <= n[1] <= self.cols-1:
        result.append(n)
    return result

  def getMineNeighbors(self, i, j):
    mines = []
    neighbors = self.getNeighbours(i, j)
    for n in neighbors:
      if self.getCell(n).mine:
        mines.append(n)
    return mines

  def getFlagNeighbors(self, i, j):
    flags = []
    neighbors = self.getNeighbours(i, j)
    for n in neighbors:
      if self.getCell(n).flag:
        flags.append(n)
    return flags

  def getHiddenNeighbors(self, i, j, ignoreFlagged=False):
    hidden = []
    neighbors = self.getNeighbours(i, j)
    for n in neighbors:
      cell = self.getCell(n)
      if cell.hidden and ((not cell.flag) if ignoreFlagged else True):
        hidden.append(n)
    return hidden

  def populate(self, start=[]):
    start_neighbours = self.getNeighbours(start[0], start[1])
    start_neighbours.append(start)
    board_coordinates = [[i, j] for i in range(self.rows) for j in range(self.cols) if not [i, j] in start_neighbours]
    mine_coordinates = sample(board_coordinates, self.mines)

    for mine in mine_coordinates:
      i, j = mine
      self.board[i][j].mine = True
      neighbors = self.getNeighbours(i, j)
      for n in neighbors:
        if n not in mine_coordinates:
          self.getCell(n).value += 1

    self.verify()

  def verify(self):
    for i in range(0, self.rows):
      for j in range(0, self.cols):
        cell = self.board[i][j]
        if not cell.mine:
          mine_neighbors = self.getMineNeighbors(i,j)
          if cell.value != len(mine_neighbors):
            print(f"Not consistent at {i},{j}!")
            exit()

  def flag(self, p):
    cell = self.getCell(p)
    if cell.hidden:
      cell.flag = not cell.flag

  def look(self, p):
    if not self.started:
      self.populate(p)
      self.started = True
    cell = self.getCell(p)
    cell.hidden = False
    flagsAround = self.getFlagNeighbors(p[0], p[1])
    if not cell.mine and cell.value - len(flagsAround) == 0:
      neighbours = self.getNeighbours(p[0], p[1])
      for n in neighbours:
        neighbour = self.getCell(n)
        if neighbour.hidden and not neighbour.flag:
          self.look(n)

def load(fileName):
  board = []
  file = open(fileName, 'r')
  lines = file.readlines()
  mines = 0
  for fileLine in lines:
    if not fileLine.strip():
      continue
    fileLine = fileLine.strip()
    boardLine = []
    for element in fileLine.split(','):
      element = element.strip()
      cellType = element[0]
      cellState = element[1]

      cell = Cell()
      if cellType == 'M':
        cell.mine = True
        mines += 1
      else:
        cell.value = int(cellType)

      if cellState == 'V':
        cell.hidden = False
      elif cellState == 'F':
        cell.flag = True

      boardLine.append(cell)
    board.append(boardLine)
  rows = len(board)
  cols = len(board[0])
  game = Game(rows, cols, mines)
  game.board = board
  game.started = True
  game.verify()
  return game
