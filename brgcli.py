#!/usr/bin/env python3

import curses
import time


path = '/sys/class/backlight/intel_backlight'

with open(f'{path}/max_brightness', 'r') as file:
    max_brg = int(file.read())

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

    # Get the initial brightness and display str
    with open(f'{path}/brightness', 'r') as file:
        display_str = file.read()
        brg_value = int(display_str)

    while True:
        screen.addstr(0, 0, display_str, curses.A_REVERSE)

        # Check for relevant keypresses
        char = screen.getch()

        if char == -1:
            time.sleep(0.1)

            # Only update brightness from file while no keys are being pressed
            with open(f'{path}/brightness', 'r') as file:
                new_str = file.read()

            if new_str != display_str:
                display_str = new_str
                brg_value = int(display_str)
                screen.erase()

        else:
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
                x = 0

            if x != 0:
                # No point in trying to increment max or decrament 0
                if x > 0 and brg_value == max_brg:
                    display_str = 'MAX'

                elif x < 0 and brg_value == 0:
                    display_str = 'MIN'

                else:
                    # Clamp brightness to multiple of 25, add x
                    brg_value = brg_value // 25 * 25 + x

                    # Cap brightness values
                    if brg_value > max_brg:
                        brg_value = max_brg
                    elif brg_value < 0:
                        brg_value = 0

                    # Write the value to the file
                    with open(f'{path}/brightness', 'w') as file:
                        file.write(str(brg_value))

                    # Update display string
                    display_str = str(brg_value)

                screen.erase()

            # Speed throttle for "keys pressed". Faster than "no keys pressed"
            time.sleep(0.03)

except KeyboardInterrupt:
    pass

finally:
    # shut down cleanly
    curses.nocbreak()
    curses.curs_set(1)
    curses.echo()
    curses.endwin()
