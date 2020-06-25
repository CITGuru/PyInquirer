# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function
import os

from .utils import print_json, format_json
from .prompt import prompt
from .separator import Separator
from .prompts.common import default_style

__version__ = '1.0.2'


def here(p):
    # TODO: Is this being used externally or deprecate?
    return os.path.abspath(os.path.join(os.path.dirname(__file__), p))
