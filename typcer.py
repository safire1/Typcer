import curses
from curses import wrapper
import time
import random
import climage

banana = climage.convert("banana.jpg")

session_stats = {
	"WPM": 0,
	"Tests": 0
	
}

def start_screen(stdscr):
	stdscr.clear()
	stdscr.addstr("\t\t\t\tWelcome to Typcer", curses.color_pair(1))
	stdscr.addstr(1, 16, '''\n\t\t,---,---,---,---,---,---,---,---,---,---,---,---,---,-------,
\t\t| ~ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 | [ | ] | <-    |
\t\t|---'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-----|
\t\t| ->| | " | , | . | P | Y | F | G | C | R | L | / | = |  \  |
\t\t|-----',--',--',--',--',--',--',--',--',--',--',--',--'-----|
\t\t| Caps | A | O | E | U | I | D | H | T | N | S | - |  Enter |
\t\t|------'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'--------|
\t\t|        | ; | Q | J | K | X | B | M | W | V | Z |          |
\t\t|------,-',--'--,'---'---'---'---'---'---'-,-'---',--,------|
\t\t| ctrl |  | alt |                          | alt  |  | ctrl |
\t\t'------'  '-----'--------------------------'------'  '------''', curses.color_pair(4))
	stdscr.addstr(13, 18, f"\n\t\tPress any key to begin!")
	stdscr.refresh()
	stdscr.getkey()

def display_text(stdscr, target, current, wpm=0):
	stdscr.addstr(f'''\n\n\t\t\t -----> Typcer <-----''', curses.color_pair(4))
	stdscr.addstr(f'''\n\t\t\t --------------------''')
	stdscr.addstr(f'''\n\t\t\t Type the text above!
                      \n\t\t\t WPM: {wpm}''', curses.color_pair(4))
	stdscr.addstr(f'''\n\t\t\t --------------------''')
	stdscr.addstr(9, 0, target)

	for i, char in enumerate(current):
		a = i
		correct_char = target[i]
		color = curses.color_pair(1)
		if char != correct_char:
			color = curses.color_pair(2)

		stdscr.addstr(9, a, char, color)

def load_text():
	with open("text.txt", "r") as f:
		lines = f.readlines()
		return random.choice(lines).strip()
	
def load_small():
	with open("short_text.txt", "r") as f:
		lines = f.readlines()
		return random.choice(lines).strip()

def wpm_test(stdscr):
	stdscr.clear()
	stdscr.addstr(1, 16, f'''\n\t\t,---,---,---,---,---,---,---,---,---,---,---,---,---,-------,
\t\t| ->| Session | - | Stats | --- | T | Y | P | C | E | R | - |
\t\t|-----',--',--',--',--',--',--',--',--',--',--',--',--'-----|
\t\t| Highest | W | P | M | : | {session_stats["WPM"]}          |
\t\t|------'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'--------|
\t\t| Number | Tests | : | {session_stats["Tests"]}             |
\t\t|------,-',--'--,'---'---'---'---'---'---'-,-'---',--,------|
\t\t|  Press  |  A  |  Long Text               | ---  |  | ---  |
\t\t|  Press  | Any |  Random Length           | ---  |  | ---  |
\t\t'------'  '-----'--------------------------'------'  '------\n
\t\t| -> | ''', curses.color_pair(1))
	
	r = stdscr.getkey()
	
	target_text = load_text() if ord(r) == 65 else load_small()
	wpm = 0
	start_time = time.time()
	current_text = []
    
	stdscr.nodelay(True)
    
    
	while True:
		time_elapsed = max(time.time() - start_time, 1)
		wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

		stdscr.clear()
		display_text(stdscr, target_text, current_text, wpm)
		if wpm > session_stats['WPM']:
			session_stats['WPM'] = wpm
		stdscr.refresh()

		if "".join(current_text) == target_text:
			stdscr.nodelay(False)
			break

		try:
			key = stdscr.getkey()
		except:
			continue

		if ord(key) == 27:
			break

		if key in ("KEY_BACKSPACE", '\b', "\x7f"):
			if len(current_text) > 0:
				current_text.pop()
		elif len(current_text) < len(target_text):
			current_text.append(key)

def main(stdscr):
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)

	start_screen(stdscr)
	while True:
		wpm_test(stdscr)
		stdscr.addstr(11, 20, "You completed the text! Press ESC to exit | Press any key to continue... ")
		session_stats["Tests"] += 1
		key = stdscr.getkey()
		
		
		
		if ord(key) == 27:
			break

wrapper(main)