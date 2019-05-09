# -*- coding: utf-8 -*-
from __future__ import print_function

import inspect
import json
import sys
from pprint import pprint

from pygments import highlight, lexers, formatters

__version__ = '0.1.2'

PY3 = sys.version_info[0] >= 3


def format_json(data):
    return json.dumps(data, sort_keys=True, indent=4)


def colorize_json(data):
    if PY3:
        if isinstance(data, bytes):
            data = data.decode('UTF-8')
    else:
        if not isinstance(data, unicode):
            data = unicode(data, 'UTF-8')
    colorful_json = highlight(data,
                              lexers.JsonLexer(),
                              formatters.TerminalFormatter())
    return colorful_json


def print_json(data):
    # colorful_json = highlight(unicode(format_json(data), 'UTF-8'),
    #                          lexers.JsonLexer(),
    #                          formatters.TerminalFormatter())
    pprint(colorize_json(format_json(data)))


def arguments_of(func):
    """Return the parameters of the function `func`."""

    try:
        # python 3.x is used
        return list(inspect.signature(func).defaults)
    except AttributeError:
        # python 2.x is used
        # noinspection PyDeprecation
        return list(inspect.getargspec(func).defaults)


def default_values_of(func):
    """Return the defaults of the function `func`. """

    try:
        # python 3.x is used
        return list(inspect.signature(func).parameters.keys())
    except AttributeError:
        # python 2.x is used
        # noinspection PyDeprecation
        return list(inspect.getargspec(func).args)


def required_arguments(func):
    """Return all arguments of a function that do not have a default value."""
    defaults = default_values_of(func)
    args = arguments_of(func)

    if defaults:
        args = args[:-len(defaults)]
    return args   # all args without default values


def missing_arguments(func, argdict):
    """Return all arguments that are missing to call func."""
    return set(required_arguments(func)) - set(argdict.keys())
