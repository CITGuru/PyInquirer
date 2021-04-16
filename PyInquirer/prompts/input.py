# -*- coding: utf-8 -*-
"""
`input` type question
"""
import inspect
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.lexers import SimpleLexer

from .common import default_style

# use std prompt-toolkit control


def question(message, **kwargs):
    default = kwargs.pop('default', '')
    validate_prompt = kwargs.pop('validate', None)
    if validate_prompt:
        if inspect.isclass(validate_prompt) and issubclass(validate_prompt, Validator):
            kwargs['validator'] = validate_prompt()
        elif callable(validate_prompt):
            class _InputValidator(Validator):
                def validate(self, document):
                    verdict = validate_prompt(document.text)
                    if not verdict == True:
                        if verdict == False:
                            verdict = 'invalid input'
                        raise ValidationError(
                            message=verdict,
                            cursor_position=len(document.text))
            kwargs['validator'] = _InputValidator()

    # TODO style defaults on detail level
    kwargs['style'] = kwargs.pop('style', default_style)
    qmark = kwargs.pop('qmark', '?')
    kwargs.setdefault('lexer', SimpleLexer('class:answer'))


    def _get_prompt_tokens():
        result = [
            ('class:questionmark', qmark),
            ('class:question', ' %s  ' % message)
        ]
        if kwargs.get('multiline'):
            result += [
                ('class:instruction', 'Multiline; finish with '),
                ('class:instruction reverse', 'Esc, ↵'),
                ('class:instruction', ' or '),
                ('class:instruction reverse', 'Alt+Enter'),
                ('class:questionmark', '\n> '),
            ]
        return result

    return prompt(
        message=_get_prompt_tokens,
        default=default,
        **kwargs
    )
