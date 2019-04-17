# brgcli
A little curses based Python tool for adjusting the screen brightness from the command line

The tool uses the files in /sys/class/backlight/ provided by the Linux Kernel ACPI module.
Currently, this only works with intel graphics, because that is what I have, hence I know 
the names of the relevant files (/sys/class/backlight/intel_backlight/{brightness,max_brightness}).

This can easily be adapted to other interfaces.

Eventualy, I hope to make this work for other graphics cards.
