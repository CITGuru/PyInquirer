# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import os

# noinspection PyUnresolvedReferences
from prompt_toolkit.validation import Validator, ValidationError

from PyInquirer.prompt import prompt
from PyInquirer.separator import Separator
from PyInquirer.utils import print_json, format_json

__version__ = '1.0.2'


def here(p):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), p))
