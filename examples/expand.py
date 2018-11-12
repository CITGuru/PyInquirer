# -*- coding: utf-8 -*-
"""
* example for expand question type
* run example by typing `python example/checkbox.py` in your console
"""
from __future__ import print_function, unicode_literals

from PyInquirer import style_from_dict, Token, prompt, print_json, Separator

from examples import custom_style_2

# questions - 
questions = [
    {
        'type': 'expand',
        'message': 'Conflict on `file.js`: ',
        'name': 'overwrite',
        'default': 'a',
        'choices': [
            {
                'key': 'y',
                'name': 'Overwrite',
                'value': 'overwrite'
            },
            {
                'key': 'a',
                'name': 'Overwrite this one and all next',
                'value': 'overwrite_all'
            },
            {
                'key': 'd',
                'name': 'Show diff',
                'value': 'diff'
            },
            Separator(),
            {
                'key': 'x',
                'name': 'Abort',
                'value': 'abort'
            }
        ]
    }
]

answers = prompt(questions, style=custom_style_2)
print_json(answers)
