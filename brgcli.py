#!/usr/bin/env python3

import curses
import time

max_brightness = 7500

path = '/sys/class/backlight/intel_backlight/'

with open(f'{path}/max_brightness', 'r') as max_file:
    max_brg = int(max_file.read())

try:
    # get the curses screen window
    screen = curses.initscr()

    # turn off input echoing, disable cursor, and respond to keys
    # immediately (don't wait for enter)
    curses.noecho()
    curses.curs_set(0)
    curses.cbreak()

    # map arrow keys to special values
    screen.keypad(1)

    # Do not wait for input
    screen.nodelay(1)

    while True:
        # First, get the current brightness:
        with open(f'{path}/brightness', 'r') as file:
            brightness = file.read()

        # Check for keypresses:
        char = screen.getch()
        if char != -1:
            if char == ord('q'):
                break
            elif char == curses.KEY_PPAGE:
                x = 250
            elif char == curses.KEY_NPAGE:
                x = -250
            elif char == curses.KEY_UP:
                x = 25
            elif char == curses.KEY_DOWN:
                x = -25

            # Add increment (x) and clamp to multiples of 25
            brightness = str(int(brightness) // 25 * 25 + x)

            # We don't want to touch the file if unless we have a valid value
            if int(brightness) > max_brg:
                brightness = str(max_brightness)
            elif int(brightness) < 0:
                brightness = '0'

            # Write the value to the file
            with open(f'{path}/brightness', 'w') as file:
                file.write(brightness)

        screen.erase()
        screen.addstr(
            0, 0, brightness, curses.A_REVERSE)

        time.sleep(0.01)

except KeyboardInterrupt:
    pass

finally:
    # shut down cleanly
    curses.nocbreak()
    curses.curs_set(1)
    curses.echo()
    curses.endwin()
