# -*- coding: utf-8 -*-
"""
* Editor prompt example
"""
from __future__ import print_function, unicode_literals

from PyInquirer import style_from_dict, Token, prompt, print_json
from PyInquirer import Validator, ValidationError
from examples import custom_style_2
from pprint import pprint


questions = [
    {
        'type': 'editor',
        'name': 'bio',
        'message': 'Please write a short bio of at least 3 lines.',
        'default': 'Hello World',
        'validate': lambda text: len(text.split('\n')) >= 3 or 'Must be at least 3 lines.',
        'eargs': {
            'editor':'default',
            'ext':'.py'
        }
    }
]

answers = prompt(questions, style=custom_style_2)
pprint(answers)
