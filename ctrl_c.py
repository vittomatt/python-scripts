#!/usr/bin/env python

import sys
import signal

def def_handler():
    print("Bye!")
    sys.exit(1)

# Ctrl+C
signal.signal(signal.SIGINT, def_handler)

# Code
if __name__ == "__main__":
    pass