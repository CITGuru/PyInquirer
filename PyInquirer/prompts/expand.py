# -*- coding: utf-8 -*-
"""
`expand` type question
"""
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.filters import IsDone
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.containers import ConditionalContainer, HSplit
from prompt_toolkit.layout.dimension import LayoutDimension as D

from . import PromptParameterException
from ..separator import Separator
from .common import default_style
from .common import if_mousedown


# custom control based on FormattedTextControl

class InquirerControl(FormattedTextControl):
    def __init__(self, choices, default=None, **kwargs):
        self.pointer_index = 0
        self.answered = False
        self._init_choices(choices, default)
        self._help_active = False  # help is activated via 'h' key
        super().__init__(self._get_choice_tokens, **kwargs)

    def _init_choices(self, choices, default=None):
        # helper to convert from question format to internal format

        self.choices = []  # list (key, name, value)

        for i, c in enumerate(choices):
            if isinstance(c, Separator):
                self.choices.append(c)
            else:
                if isinstance(c, str):
                    self.choices.append((key, c, c))
                else:
                    key = c.get('key')
                    name = c.get('name')
                    value = c.get('value', name)
                    self.choices.append([key, name, value])

        # append the help choice
        self.choices.append(['h', 'Help, list all options', '__HELP__'])

        # set the default
        for i, choice in enumerate(self.choices):
            if isinstance(choice, list):
                key = choice[0]
                default = default or "h"
                if default == key:
                    self.pointer_index = i
                    choice[0] = key.upper()  # default key is in uppercase

    @property
    def choice_count(self):
        return len(self.choices)

    def _get_choice_tokens(self):
        tokens = []

        def _append(index, line):
            if isinstance(line, Separator):
                tokens.append(('class:separator', '   %s\n' % line))
            else:
                key = line[0]
                line = line[1]
                pointed_at = (index == self.pointer_index)

                @if_mousedown
                def select_item(mouse_event):
                    # bind option with this index to mouse event
                    self.pointer_index = index

                if pointed_at:
                    tokens.append(('class:selected', '  %s) %s' % (key, line),
                                   select_item))
                else:
                    tokens.append(('', '  %s) %s' % (key, line),
                                   select_item))
                tokens.append(('', '\n'))

        if self._help_active:
            # prepare the select choices
            for i, choice in enumerate(self.choices):
                _append(i, choice)
            tokens.append(('', '  Answer: %s' %
                           self.choices[self.pointer_index][0]))
        else:
            tokens.append(('class:pointer', '>> '))
            tokens.append(('', self.choices[self.pointer_index][1]))
        return tokens

    def get_selected_value(self):
        # get value not label
        return self.choices[self.pointer_index][2]


def question(message, **kwargs):
    # TODO extract common parts for list, checkbox, rawlist, expand
    # TODO up, down navigation
    if not 'choices' in kwargs:
        raise PromptParameterException('choices')

    choices = kwargs.pop('choices', None)
    default = kwargs.pop('default', None)
    qmark = kwargs.pop('qmark', '?')
    # TODO style defaults on detail level
    style = kwargs.pop('style', default_style)

    ic = InquirerControl(choices, default)

    def get_prompt_tokens():
        tokens = []

        tokens.append(('class:questionmark', qmark))
        tokens.append(('class:question', ' %s ' % message))
        if not ic.answered:
            tokens.append(('class:instruction', ' (%s)' % ''.join(
                [k[0] for k in ic.choices if not isinstance(k, Separator)])))
        else:
            tokens.append(('class:answer', ' %s' % ic.get_selected_value()))
        return tokens

    #@Condition
    #def is_help_active():
    #    return ic._help_active

    # assemble layout
    layout = HSplit([
        Window(height=D.exact(1),
               content=FormattedTextControl(get_prompt_tokens)
        ),
        ConditionalContainer(
            Window(ic),
            #filter=is_help_active & ~IsDone()  # ~ bitwise inverse
            filter=~IsDone()  # ~ bitwise inverse
        )
    ])

    # key bindings
    kb = KeyBindings()

    @kb.add('c-q', eager=True)
    @kb.add('c-c', eager=True)
    def _(event):
        raise KeyboardInterrupt()

    # add key bindings for choices
    for i, c in enumerate(ic.choices):
        if not isinstance(c, Separator):
            def _reg_binding(i, keys):
                # trick out late evaluation with a "function factory":
                # http://stackoverflow.com/questions/3431676/creating-functions-in-a-loop
                @kb.add(keys, eager=True)
                def select_choice(event):
                    ic.pointer_index = i
            if c[0] not in ['h', 'H']:
                _reg_binding(i, c[0])
                if c[0].isupper():
                    _reg_binding(i, c[0].lower())

    @kb.add('H', eager=True)
    @kb.add('h', eager=True)
    def help_choice(event):
        ic._help_active = not ic._help_active

    @kb.add('enter', eager=True)
    def set_answer(event):
        selected_value = ic.get_selected_value()
        if selected_value == '__HELP__':
            ic._help_active = True
        else:
            ic.answered = True
            event.app.exit(result=selected_value)

    return Application(
        layout=Layout(layout),
        key_bindings=kb,
        mouse_support=True,
        style=style
    )
