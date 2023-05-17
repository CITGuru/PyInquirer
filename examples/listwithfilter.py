# -*- coding: utf-8 -*-
"""
list prompt example
"""
from __future__ import print_function, unicode_literals

from pprint import pprint

from PyInquirer import prompt, Separator

from examples import custom_style_2



def get_delivery_options(answers):
    options = ['bike', 'car', 'truck']
    if answers['size'] == 'jumbo':
        options.append('helicopter')
    return options


questions = [
    {
        'type': 'listwithfilter',
        'name': 'theme',
        'message': 'What do you want to do?',
        'choices': [
            'Order a pizza',
            'Make a reservation',
            Separator(),
            'Ask for opening hours',
            {
                'name': 'Contact support',
                'disabled': 'Unavailable at this time'
            },
            'Talk to the receptionist'
        ]
    },
    {
        'type': 'listwithfilter',
        'name': 'size',
        'message': 'What size do you need?',
        'choices': ['Jumbo', 'Large', 'Standard', 'Medium', 'Small', 'Micro'],
        'filter': lambda val: val.lower()
    },
    {
        'type': 'listwithfilter',
        'name': 'cook_level',
        'message': 'How well done do you want it?',
        'choices': [
            {'name': 'Crispy', 'value': 'crispy'},
            {'name': 'Normal', 'value': 'normal'},
            {'name': 'Soft', 'value': 'soft'}],
        'default': 'crispy'
    },
    {
        'type': 'listwithfilter',
        'name': 'delivery',
        'message': 'Which vehicle you want to use for delivery?',
        'choices': get_delivery_options,
    },
]

answers = prompt.prompt(questions, style=custom_style_2)
pprint(answers)
