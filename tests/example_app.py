# -*- coding: utf-8 -*-
"""
example app to test running an app as subprocess within pty
"""
from __future__ import print_function, unicode_literals
import sys, time


PY3 = sys.version_info[0] >= 3

if PY3:
    raw_input = input


# http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main():
    print('hi, there!')
    time.sleep(0.010)
    print('let\'s get to know each other better...')
    name = raw_input("Please enter your name: ")
    print(bcolors.BOLD + bcolors.UNDERLINE + 'Hi %s, have a nice day!' % name +
          bcolors.ENDC)
    print('It was a pleasure talking to you...')


if __name__ == '__main__':
    main()
