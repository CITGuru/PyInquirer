# -*- coding: utf-8 -*-
"""
When example
"""
from __future__ import print_function, unicode_literals

from PyInquirer import style_from_dict, Token, prompt, print_json

from examples import custom_style_2


def dislikes_bacon(answers):
    # demonstrate use of a function... here a lambda function would be enough
    return not answers['bacon']


questions = [
    {
        'type': 'confirm',
        'name': 'bacon',
        'message': 'Do you like bacon?'
    },
    {
        'type': 'input',
        'name': 'favorite',
        'message': 'Bacon lover, what is your favorite type of bacon?',
        'when': lambda answers: answers['bacon']
    },
    {
        'type': 'confirm',
        'name': 'pizza',
        'message': 'Ok... Do you like pizza?',
        'default': False,  # only for demo :)
        'when': dislikes_bacon
    },
    {
        'type': 'input',
        'name': 'favorite',
        'message': 'Whew! What is your favorite type of pizza?',
        'when': lambda answers: answers.get('pizza', False)
    }
]

answers = prompt(questions, style=custom_style_2)

print_json(answers)
