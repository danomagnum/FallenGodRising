import curses

UP = [curses.KEY_UP, ord('k'), ord('w')]
DOWN = [curses.KEY_DOWN, ord('j'), ord('s')]
LEFT = [curses.KEY_LEFT, ord('h'), ord('a')]
RIGHT = [curses.KEY_RIGHT, ord('l'), ord('d')]
SELECT = [curses.KEY_ENTER, 10, ord(' ')]
BACK = [curses.KEY_BACKSPACE, 127, -1]