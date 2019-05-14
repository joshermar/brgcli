#!/usr/bin/env python3
import curses
import time


def get_value(filename, path='/sys/class/backlight/intel_backlight'):
    """Return an int from path/filename"""
    with open(f'{path}/{filename}', 'r') as file:
        return int(file.read())


def set_value(value, filename, path='/sys/class/backlight/intel_backlight'):
    """Writes value to path/filename.
    Obviously, value should be a string of an acceptable value.
    """
    with open(f'{path}/{filename}', 'w') as file:
        file.write(str(value))


def clamp_and_bound(brg_value, increment):
    """Returns int, divisble by 25 between 0 and max (inclusive).
    brg_value can be any value but increment should already be divisble by 25.
    """
    brg_value = brg_value // 25 * 25 + increment
    if brg_value > max_brg:
        brg_value = max_brg
    elif brg_value < 0:
        brg_value = 0
    return brg_value


# char values conveniently maped to increments
char_mappings = {
    curses.KEY_PPAGE: 250,
    curses.KEY_NPAGE: -250,
    curses.KEY_UP: 25,
    curses.KEY_DOWN: -25}

try:
    # Set up curses screen window
    screen = curses.initscr()

    curses.noecho()     # Disable input echoing
    curses.curs_set(0)  # Disable cursor
    curses.cbreak()     # don't wait for enter
    screen.keypad(1)    # Map arrow keys to special values
    screen.nodelay(1)   # Do not wait for input

    # Initial values
    max_brg = get_value('max_brightness')
    brg_value = get_value('brightness')
    display_str = str(brg_value)

    char = -1

    while char not in (81, 113):
        screen.addstr(0, 0, display_str, curses.A_REVERSE)

        char = screen.getch()

        if char == -1:
            brg_value = get_value('brightness')
            display_str = str(brg_value)

            time.sleep(0.1)   # Speed throttle for "no-keys-pressed"
            screen.erase()

        else:
            increment = char_mappings.get(char)

            if increment:
                # Shows MAX/MIN message if trying to go out of bounds
                if increment > 0 and brg_value == max_brg:
                    display_str = 'MAX'
                elif increment < 0 and brg_value == 0:
                    display_str = 'MIN'

                else:
                    brg_value = clamp_and_bound(brg_value, increment)
                    set_value(brg_value, 'brightness')
                    display_str = str(brg_value)

                screen.erase()

            time.sleep(0.03)    # Speed throttle for "keys pressed"

except KeyboardInterrupt:
    pass

finally:
    # shut down cleanly
    curses.nocbreak()
    curses.curs_set(1)
    curses.echo()
    curses.endwin()
