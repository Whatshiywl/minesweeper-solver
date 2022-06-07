import numpy as np
from random import sample
from game import Game

precision = 1e-6

def getCells(game: Game):
  unknowns = []
  numbered = []
  for i in range(game.rows):
    for j in range(game.cols):
      pos = [i, j]
      cell = game.getCell(pos)
      if cell.hidden and not cell.flag:
        unknowns.append(pos)
      if not cell.hidden and cell.value > 0:
        hiddenAround = game.getHiddenNeighbors(i, j, ignoreFlagged=True)
        if (len(hiddenAround)):
          numbered.append(pos)
  return (unknowns, numbered)

def generateMatrix(game: Game, unknowns, numbered):
  a = []
  b = []

  a.append([1] * len(unknowns))
  totalFlagged = 0
  for i in range(game.rows):
    for j in range(game.cols):
      cell = game.getCell([i, j])
      if cell.flag:
        totalFlagged += 1
  b.append(game.mines - totalFlagged)

  for n in numbered:
    line = [0] * len(unknowns)
    hidden = game.getHiddenNeighbors(n[0], n[1], ignoreFlagged=True)
    for h in hidden:
      if not h in unknowns:
        print("Something is wrong here!")
        exit()
      index = unknowns.index(h)
      line[index] = 1
    a.append(line)

    cell = game.getCell(n)
    flagged = game.getFlagNeighbors(n[0], n[1])
    remaining = cell.value - len(flagged)
    b.append(remaining)
  return (a, b)

def mapSolution(value):
  if value + precision > 1:
    return 1
  if value - precision < 0:
    return 0
  return value

def solve(game: Game):
  (unknowns, numbered) = getCells(game)
  (a, b) = generateMatrix(game, unknowns, numbered)
  r = np.linalg.lstsq(a, b, rcond=None)
  solution = r[0]
  mapped = tuple(zip(unknowns, [mapSolution(x) for x in solution]))

  toFlag = [x for x in mapped if x[1] == 1]
  if len(toFlag):
    return sample(toFlag, 1)[0]

  toLook = [x for x in mapped if x[1] == 0]
  if (len(toLook)):
    return sample(toLook, 1)[0]

  return None
