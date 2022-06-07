class Cell:
  mine = False
  value = 0
  flag = False
  hidden = True

  def toString(self, reveal=False):
    valueChar = "\033[31m*\033[0m" if self.mine else (
      str(self.value) if self.value > 0 else "."
    )
    if (reveal):
      return valueChar
    return "\033[33mF\033[0m" if self.flag else (
      " " if self.hidden else valueChar
    )
