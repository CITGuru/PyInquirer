# -*- coding: utf-8 -*-
"""
`password` type question
"""
from . import input 

# use std prompt-toolkit control


def question(message, **kwargs):
    kwargs['is_password'] = True
    return input.question(message, **kwargs)
