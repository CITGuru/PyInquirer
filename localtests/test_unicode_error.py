# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from PyInquirer import prompt

def main():
    choice = 'John’s Pizza'
    questions = [
        {
            'type': 'list',
            'name': 'pizza',
            'message': 'Pizzeria:',
            'choices' : [choice]
        }
    ]
    answer = prompt(questions)
    pizza = answer['pizza']
    print('Answer is |' + pizza + '|' )

if __name__ == '__main__':
    main()