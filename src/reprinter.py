# Credits to Bouke Versteegh!
# I made no attempt to figure out how this works, because it 'just worked'!
# Source: https://stackoverflow.com/a/15586020
import re, sys

class Reprinter:
  def __init__(self):
    self.text = ''

  def moveup(self, lines):
    for _ in range(lines):
      sys.stdout.write("\x1b[A")

  def reprint(self, text):
    # Clear previous text by overwritig non-spaces with spaces
    self.moveup(self.text.count("\n"))
    sys.stdout.write(re.sub(r"[^\s]", " ", self.text))

    # Print new text
    lines = min(self.text.count("\n"), text.count("\n"))
    self.moveup(lines)
    sys.stdout.write(text)
    self.text = text
