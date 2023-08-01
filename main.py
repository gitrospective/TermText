import curses
from curses import wrapper
import time
import random


def start_screen(stdscr):
	stdscr.clear()
	stdscr.addstr("Welcome to the Speed Typing Test!")
	stdscr.addstr("\nPress any key to begin!")
	stdscr.refresh()
	stdscr.getkey()

def load_text():
	with open("text.txt", "r") as f:
		lines = f.readlines()
		return random.choice(lines).strip()

def display(stdscr, target, current, wpm = 0):
    stdscr.addstr(target)
    #stdscr.addstr(1, 0, f"WPM: {wpm}")
    
    for i, ch in enumerate(current):
        correct = target[i]
        color = curses.color_pair(1)
        if ch != correct:
            color = curses.color_pair(2)
        stdscr.addstr(0, i, ch, color)

def test(stdscr):
    target = "Hello world this is some test text for this app!"
    current =[]
    wpm = 0
    start = time.time()
    stdscr.nodelay(True)
    while True:
        elapsed = max(time.time() - start, 1)
        wpm = round((len(current)/(elapsed/60)) / 5)
        stdscr.clear()
        display(stdscr, target, current, wpm)
        stdscr.addstr(1, 0, f"WPM: {wpm}")
        stdscr.refresh()
        
        if "".join(current) == target:
            stdscr.nodelay(False)
            break
        
        try:
            key = stdscr.getkey()
        except:
            continue

        if len(key) == 1 and ord(key) == 27:
            break

        if key in ("KEY_BACKSPACE", '\b', '\x7f'):
            if len(current) > 0:
                current.pop()
        elif len(current) < len(target):
            current.append(key)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK) 
    start_screen(stdscr)
    test(stdscr)
    stdscr.addstr(2, 0, "Completed! Press any key to continue")

wrapper(main)
