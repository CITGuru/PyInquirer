# -*- coding: utf-8 -*-
"""
* password question example
"""
from __future__ import print_function, unicode_literals

from PyInquirer import style_from_dict, Token, prompt, print_json


style = style_from_dict({
    Token.QuestionMark: '#FF9D00 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#5F819D bold',
    Token.Question: '',
})


questions = [
    {
        'type': 'password',
        'message': 'Enter your git password',
        'name': 'password'
    }
]

answers = prompt(questions, style=style)
print_json(answers)
