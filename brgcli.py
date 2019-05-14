#!/usr/bin/env python3

import curses
import time


path = '/sys/class/backlight/intel_backlight'

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

    testvar = 0

    while True:
        # Get the current brightness
        with open(f'{path}/brightness', 'r') as file:
            brightness = int(file.read())

        screen.erase()
        screen.addstr(0, 0, str(brightness), curses.A_REVERSE)

        x = 0

        # Check for relevant keypresses
        char = screen.getch()

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

        if not (brightness == 0 and x < 0 or
                brightness == max_brg and x > 0):

            # Clamp brightness to multiple of 25, add x
            brightness = brightness // 25 * 25 + x

            # Cap increment
            if brightness > max_brg:
                brightness = max_brg
            elif brightness < 0:
                brightness = '0'

            # Write the value to the file
            with open(f'{path}/brightness', 'w') as file:
                file.write(str(brightness))

        time.sleep(0.05)

except KeyboardInterrupt:
    pass

finally:
    # shut down cleanly
    curses.nocbreak()
    curses.curs_set(1)
    curses.echo()
    curses.endwin()
