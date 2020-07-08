# -*- coding: utf-8 -*-
"""
`rawlist` type question
"""
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.filters import IsDone
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.containers import ConditionalContainer, HSplit
from prompt_toolkit.layout.dimension import LayoutDimension as D

from prompt_toolkit.layout import Layout


from . import PromptParameterException
from ..separator import Separator
from .common import default_style
from .common import if_mousedown


# custom control based on FormattedTextControl

class InquirerControl(FormattedTextControl):
    def __init__(self, choices, **kwargs):
        self.pointer_index = 0
        self.answered = False
        self._init_choices(choices)
        super().__init__(self._get_choice_tokens, **kwargs)

    def _init_choices(self, choices):
        # helper to convert from question format to internal format
        self.choices = []  # list (key, name, value)
        searching_first_choice = True
        key = 1  # used for numeric keys
        for i, c in enumerate(choices):
            if isinstance(c, Separator):
                self.choices.append(c)
            else:
                if isinstance(c, str):
                    self.choices.append((key, c, c))
                    key += 1
                if searching_first_choice:
                    self.pointer_index = i  # found the first choice
                    searching_first_choice = False

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
                    tokens.append(('class:selected', '  %d) %s' % (key, line),
                                   select_item))
                else:
                    tokens.append(('', '  %d) %s' % (key, line),
                                   select_item))

                tokens.append(('', '\n'))

        # prepare the select choices
        for i, choice in enumerate(self.choices):
            _append(i, choice)
        tokens.append(('', '  Answer: %d' % self.choices[self.pointer_index][0]))
        return tokens

    def get_selected_value(self):
        # get value not label
        return self.choices[self.pointer_index][2]


def question(message, **kwargs):
    # TODO extract common parts for list, checkbox, rawlist, expand
    if not 'choices' in kwargs:
        raise PromptParameterException('choices')
    # this does not implement default, use checked...
    # TODO
    #if 'default' in kwargs:
    #    raise ValueError('rawlist does not implement \'default\' '
    #                     'use \'checked\':True\' in choice!')
    qmark = kwargs.pop('qmark', '?')
    choices = kwargs.pop('choices', None)
    if len(choices) > 9:
        raise ValueError('rawlist supports only a maximum of 9 choices!')

    # TODO style defaults on detail level
    style = kwargs.pop('style', default_style)

    ic = InquirerControl(choices)

    def get_prompt_tokens():
        tokens = []

        tokens.append(('class:questionmark', qmark))
        tokens.append(('class:question', ' %s ' % message))
        if ic.answered:
            tokens.append(('class:answer', ' %s' % ic.get_selected_value()))
        return tokens

    # assemble layout
    layout = HSplit([
        Window(height=D.exact(1),
               content=FormattedTextControl(get_prompt_tokens)
        ),
        ConditionalContainer(
            Window(ic),
            filter=~IsDone()
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
            _reg_binding(i, '%d' % c[0])

    @kb.add('enter', eager=True)
    def set_answer(event):
        ic.answered = True
        event.app.exit(result=ic.get_selected_value())

    return Application(
        layout=Layout(layout),
        key_bindings=kb,
        mouse_support=True,
        style=style
    )
