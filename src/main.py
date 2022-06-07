from game import Game, load
from solver import solve
import keyboard

rows = 15
cols = 15
mines = 20
fileName = ""
game = None

inputInfo = input("Enter 'rows,cols,mines', nothing for default values (15,15,20) or the name of a valid board file: ").split(',')
if len(inputInfo) == 3:
  rows = int(inputInfo[0])
  cols = int(inputInfo[1])
  mines = int(inputInfo[2])
elif len(inputInfo) == 1:
  fileName = inputInfo[0]
elif len(inputInfo) == 0:
  pass
else:
  print("Invalid input!")
  exit()

if fileName:
  game = load(fileName)
else:
  game = Game(rows, cols, mines)

pos = [int(game.rows/2), int(game.cols/2)]

ignore = { }

while (True):
  game.printBoard(highlightPos=pos)
  key = keyboard.read_key()
  isIgnoring = key in ignore and ignore[key]
  if not isIgnoring:
    if key == "esc":
      exit()
    if key == "up" and pos[0] > 0:
      pos[0] -= 1
    if key == "down" and pos[0] < game.rows - 1:
      pos[0] += 1
    if key == "left" and pos[1] > 0:
      pos[1] -= 1
    if key == "right" and pos[1] < game.cols - 1:
      pos[1] += 1
    if key == "f":
      game.flag(pos)
    if key == "space":
      game.look(pos)
    if key == "s":
      result = solve(game)
      if result == None:
        continue
      pos = result[0]
      if result[1] == 1:
        game.flag(pos)
      elif result[1] == 0:
        game.look(pos)
  ignore[key] = not isIgnoring
