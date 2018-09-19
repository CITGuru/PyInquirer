# -*- coding: utf-8 -*-
"""
* password question example
"""
from __future__ import print_function, unicode_literals

from PyInquirer import style_from_dict, Token, prompt, print_json

from examples import custom_style_2


questions = [
    {
        'type': 'password',
        'message': 'Enter your git password',
        'name': 'password'
    }
]

answers = prompt(questions, style=custom_style_2)
print_json(answers)
