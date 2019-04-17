#!/usr/bin/env python3

import curses

# Set max brightness value
max_brightness = 7500

# Read initial brightness value
with open('/sys/class/backlight/intel_backlight/brightness', 'r') as file:
    brightness = file.read()

brightness = round(int(brightness) / 25) * 25

try:
    # get the curses screen window
    screen = curses.initscr()

    # turn off input echoing, disable cursor, and respond to keys
    # immediately (don't wait for enter)
    curses.noecho()
    curses.curs_set(0)
    curses.cbreak()

    # map arrow keys to special values
    screen.keypad(True)

    # Initial screen... :/
    screen.addstr(
        0, 0, 'Current brightness: ' + str(brightness), curses.A_REVERSE)

    while True:
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
        else:
            continue

        # make sure it doesnt go over max or under 0
        brightness += x
        if brightness > max_brightness:
            brightness = max_brightness
        elif brightness < 0:
            brightness = 0

        # Write the value to the file and display new current value
        with open(
            '/sys/class/backlight/intel_backlight/brightness', 'w'
        ) as file:
            file.write(str(brightness))
        screen.erase()
        screen.addstr(
            0, 0, 'Current brightness: ' + str(brightness), curses.A_REVERSE)

except KeyboardInterrupt:
    pass

finally:
    # shut down cleanly
    curses.nocbreak()
    curses.echo()
    curses.curs_set(1)
    curses.endwin()
