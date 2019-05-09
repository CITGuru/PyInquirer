# -*- coding: utf-8 -*-
"""
`input` type question
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys

import inspect
from prompt_toolkit.styles import merge_styles
from prompt_toolkit.application import Application
from prompt_toolkit import PromptSession

from prompt_toolkit.validation import Validator, ValidationError
# from prompt_toolkit.layout.lexers import SimpleLexer
from prompt_toolkit.layout import FormattedTextControl, Layout
from PyInquirer.constants import NO_OR_YES, YES, NO, YES_OR_NO, DEFAULT_STYLE
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys

# use std prompt-toolkit control


def question(message,
            qmark="?",
            default=True,
            style=None,
            **kwargs):

    merged_style = merge_styles([DEFAULT_STYLE, style])

    default = kwargs.pop('default', '')
    print(default)
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
    kwargs['style'] = kwargs.pop('style', merged_style)
    qmark = kwargs.pop('qmark', qmark)


    def get_prompt_tokens():
        tokens = []

        tokens.append(("class:qmark", qmark))
        tokens.append(("class:question", ' {} '.format(message)))
        tokens.append(("class:answer", default))
        

        return tokens

    # bindings = KeyBindings()

    # @bindings.add(Keys.ControlQ, eager=True)
    # @bindings.add(Keys.ControlC, eager=True)
    # def _(event):
    #     raise KeyboardInterrupt()

    return PromptSession(get_prompt_tokens,
        # key_bindings=bindings,
        # style=merged_style,
        **kwargs
    ).app
