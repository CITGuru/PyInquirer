# -*- coding: utf-8 -*-
"""
`list` type question
"""
from prompt_toolkit.application import Application, get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.filters import IsDone
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.containers import ConditionalContainer, HSplit
from prompt_toolkit.layout.dimension import LayoutDimension as D
from prompt_toolkit.layout import Layout

from . import PromptParameterException
from ..separator import Separator
from .common import if_mousedown, default_style

# custom control based on FormattedTextControl
# docu here:
# https://github.com/jonathanslenders/python-prompt-toolkit/issues/281
# https://github.com/jonathanslenders/python-prompt-toolkit/blob/master/examples/full-screen-layout.py
# https://github.com/jonathanslenders/python-prompt-toolkit/blob/master/docs/pages/full_screen_apps.rst


class InquirerControl(FormattedTextControl):
    def __init__(self, choices, default, **kwargs):
        self.selected_option_index = 0
        self.answered = False
        self.choices = choices
        self._init_choices(choices, default)
        super().__init__(self._get_choice_tokens, **kwargs)

    def _init_choices(self, choices, default):
        # helper to convert from question format to internal format
        self.choices = []  # list (name, value, disabled)
        searching_first_choice = True
        for i, c in enumerate(choices):
            if isinstance(c, Separator):
                self.choices.append((c, None, None))
            else:
                if isinstance(c, str):
                    self.choices.append((c, c, None))
                else:
                    name = c.get('name')
                    value = c.get('value', name)
                    disabled = c.get('disabled', None)
                    self.choices.append((name, value, disabled))
                    if value == default:
                        self.selected_option_index = i
                        searching_first_choice = False
                if searching_first_choice:
                    self.selected_option_index = i  # found the first choice
                    searching_first_choice = False
                if default and (default == i or default == c):
                    self.selected_option_index = i  # default choice exists
                    searching_first_choice = False

    @property
    def choice_count(self):
        return len(self.choices)

    def _get_choice_tokens(self):
        tokens = []

        def append(index, choice):
            selected = (index == self.selected_option_index)

            @if_mousedown
            def select_item(mouse_event):
                # bind option with this index to mouse event
                self.selected_option_index = index
                self.answered = True
                get_app().exit(result=self.get_selection()[0])

            if isinstance(choice[0], Separator):
                tokens.append(('class:separator', '  %s\n' % choice[0]))
            else:
                tokens.append(('class:pointer' if selected else '', ' \u276f ' if selected
                else '   '))
                if selected:
                    tokens.append(('[SetCursorPosition]', ''))
                if choice[2]:  # disabled
                    tokens.append(('class:Selected' if selected else '',
                                   '- %s (%s)' % (choice[0], choice[2])))
                else:
                    try:
                        tokens.append(('class:Selected' if selected else '', str(choice[0]),
                                    select_item))
                    except:
                        tokens.append(('class:Selected' if selected else '', choice[0],
                                    select_item))
                tokens.append(('', '\n'))

        # prepare the select choices
        for i, choice in enumerate(self.choices):
            append(i, choice)
        tokens.pop()  # Remove last newline.
        return tokens

    def get_selection(self):
        return self.choices[self.selected_option_index]


def question(message, **kwargs):
    # TODO disabled, dict choices
    if not 'choices' in kwargs:
        raise PromptParameterException('choices')

    choices = kwargs.pop('choices', None)
    default = kwargs.pop('default', None)
    qmark = kwargs.pop('qmark', '?')
    # TODO style defaults on detail level
    style = kwargs.pop('style', default_style)

    ic = InquirerControl(choices, default=default)

    def get_prompt_tokens():
        tokens = []

        tokens.append(('class:questionmark', qmark))
        tokens.append(('class:question', ' %s ' % message))
        if ic.answered:
            tokens.append(('class:answer', ' ' + ic.get_selection()[0]))
        else:
            tokens.append(('class:instruction', ' (Use arrow keys)'))
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
        # event.app.exit(result=None)

    @kb.add('down', eager=True)
    def move_cursor_down(event):
        def _next():
            ic.selected_option_index = (
                (ic.selected_option_index + 1) % ic.choice_count)
        _next()
        while isinstance(ic.choices[ic.selected_option_index][0], Separator) or\
                ic.choices[ic.selected_option_index][2]:
            _next()

    @kb.add('up', eager=True)
    def move_cursor_up(event):
        def _prev():
            ic.selected_option_index = (
                (ic.selected_option_index - 1) % ic.choice_count)
        _prev()
        while isinstance(ic.choices[ic.selected_option_index][0], Separator) or \
                ic.choices[ic.selected_option_index][2]:
            _prev()

    @kb.add('enter', eager=True)
    def set_answer(event):
        ic.answered = True
        event.app.exit(result=ic.get_selection()[1])

    return Application(
        layout=Layout(layout),
        key_bindings=kb,
        mouse_support=False,
        style=style
    )
