#!/usr/bin/env python3

import curses

# get the curses screen window
screen = curses.initscr()

# turn off input echoing and disable cursor
curses.noecho()
curses.curs_set(0)

# respond to keys immediately (don't wait for enter)
curses.cbreak()

# map arrow keys to special values
screen.keypad(True)

# Set max brightness value
max_brightness = 7500

# Read initial brightness value
with open('/sys/class/backlight/intel_backlight/brightness', 'r') as file:
    brightness = file.read()

screen.addstr(0, 0, 'Current brightness: ' + str(brightness), curses.A_REVERSE)

brightness = round(int(brightness) / 25) * 25

try:
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
finally:
    # shut down cleanly
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.curs_set(1)
    curses.endwin()
