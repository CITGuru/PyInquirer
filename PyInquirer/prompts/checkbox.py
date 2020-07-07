# -*- coding: utf-8 -*-
"""
`checkbox` type question
"""
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.filters import IsDone
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.containers import ConditionalContainer, \
    ScrollOffsets, HSplit, Window, WindowAlign
from prompt_toolkit.layout.dimension import LayoutDimension as D

from prompt_toolkit.layout import Layout


from . import PromptParameterException
from ..separator import Separator
from .common import setup_simple_validator, default_style, if_mousedown


# custom control based on FormattedTextControl


class InquirerControl(FormattedTextControl):
    def __init__(self, choices, pointer_index, **kwargs):
        self.pointer_index = pointer_index
        self.pointer_sign = kwargs.pop("pointer_sign", "\u276f")
        self.selected_sign = kwargs.pop("selected_sign", "\u25cf")
        self.unselected_sign = kwargs.pop("unselected_sign", "\u25cb")
        self.selected_options = []  # list of names
        self.answered = False
        self.answered_correctly = True
        self.error_message = None
        self._init_choices(choices)
        super().__init__(self._get_choice_tokens, **kwargs)

    def _init_choices(self, choices):
        # helper to convert from question format to internal format
        self.choices = []  # list (name, value)
        searching_first_choice = True if self.pointer_index == 0 else False
        for i, c in enumerate(choices):
            if isinstance(c, Separator):
                self.choices.append(c)
            else:
                name = c['name']
                value = c.get('value', name)
                disabled = c.get('disabled')
                description = c.get('description', None)
                if c.get('checked') and not disabled:
                    self.selected_options.append(value)
                self.choices.append((name, value, disabled, description))
                if searching_first_choice and not disabled:  # find the first (available) choice
                    self.pointer_index = i
                    searching_first_choice = False

    @property
    def choice_count(self):
        return len(self.choices)

    def _get_choice_tokens(self):
        tokens = []

        def append(index, line):
            if isinstance(line, Separator):
                tokens.append(('class:Separator', '  %s\n' % line))
            else:
                line_name = line[0]
                line_value = line[1]
                selected = (line_value in self.selected_options)  # use value to check if option has been selected
                pointed_at = (index == self.pointer_index)

                @if_mousedown
                def select_item(mouse_event):
                    # bind option with this index to mouse event
                    if line_value in self.selected_options:
                        self.selected_options.remove(line_value)
                    else:
                        self.selected_options.append(line_value)

                if pointed_at:
                    tokens.append(('class:pointer', ' {}'.format(self.pointer_sign), select_item))  # ' >'
                else:
                    tokens.append(('', '  ', select_item))
                # 'o ' - FISHEYE
                if choice[2]:  # disabled
                    tokens.append(('', '- %s (%s)' % (choice[0], choice[2])))
                else:
                    if selected:
                        tokens.append(('class:selected', '{} '.format(self.selected_sign), select_item))
                    else:
                        tokens.append(('', '{} '.format(self.unselected_sign), select_item))

                    if pointed_at:
                        tokens.append(('[SetCursorPosition]', ''))

                    if choice[3]:  # description
                        tokens.append(('', "%s - %s" % (line_name, choice[3])))
                    else:
                        tokens.append(('', line_name, select_item))
                tokens.append(('', '\n'))

        # prepare the select choices
        for i, choice in enumerate(self.choices):
            append(i, choice)
        tokens.pop()  # Remove last newline.
        return tokens

    def get_selected_values(self):
        # get values not labels
        return [c[1] for c in self.choices if not isinstance(c, Separator) and
                c[1] in self.selected_options]

    @property
    def line_count(self):
        return len(self.choices)


def question(message, **kwargs):
    # TODO add bottom-bar (Move up and down to reveal more choices)
    # TODO extract common parts for list, checkbox, rawlist, expand
    # TODO validate
    if not 'choices' in kwargs:
        raise PromptParameterException('choices')
    # this does not implement default, use checked...
    if 'default' in kwargs:
        raise ValueError('Checkbox does not implement \'default\' '
                         'use \'checked\':True\' in choice!')

    choices = kwargs.pop('choices', None)
    validator = setup_simple_validator(kwargs)

    # TODO style defaults on detail level
    style = kwargs.pop('style', default_style)

    pointer_index = kwargs.pop('pointer_index', 0)
    additional_parameters = dict()
    additional_parameters.update({"pointer_sign": kwargs.pop('pointer_sign', '\u276f')})
    additional_parameters.update({"selected_sign": kwargs.pop('selected_sign', '\u25cf')})
    additional_parameters.update({"unselected_sign": kwargs.pop('unselected_sign', '\u25cb')})

    ic = InquirerControl(choices, pointer_index, **additional_parameters)
    qmark = kwargs.pop('qmark', '?')

    def get_prompt_tokens():
        tokens = []

        tokens.append(('class:questionmark', qmark))
        tokens.append(('class:question', ' %s ' % message))
        if ic.answered:
            nbr_selected = len(ic.selected_options)
            if nbr_selected == 0:
                tokens.append(('class:answer', ' done'))
            elif nbr_selected == 1:
                tokens.append(('class:Answer', ' [%s]' % ic.selected_options[0]))
            else:
                tokens.append(('class:answer',
                               ' done (%d selections)' % nbr_selected))
        else:
            tokens.append(('class:instruction',
                           ' (<up>, <down> to move, <space> to select, <a> '
                           'to toggle, <i> to invert)'))
            if not ic.answered_correctly:
                tokens.append((Token.Error, ' Error: %s' % ic.error_message))
        return tokens

    # assemble layout
    layout = HSplit([
        Window(height=D.exact(1),
               content=FormattedTextControl(get_prompt_tokens),
               align=WindowAlign.CENTER,
        ),
        ConditionalContainer(
            Window(
                ic,
                width=D.exact(43),
                height=D(min=3),
                scroll_offsets=ScrollOffsets(top=1, bottom=1)
            ),
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

    @kb.add(' ', eager=True)
    def toggle(event):
        pointed_choice = ic.choices[ic.pointer_index][1]  # value
        if pointed_choice in ic.selected_options:
            ic.selected_options.remove(pointed_choice)
        else:
            ic.selected_options.append(pointed_choice)

    @kb.add('i', eager=True)
    def invert(event):
        inverted_selection = [c[1] for c in ic.choices if
                              not isinstance(c, Separator) and
                              c[1] not in ic.selected_options and
                              not c[2]]
        ic.selected_options = inverted_selection

    @kb.add('a', eager=True)
    def all(event):
        all_selected = True  # all choices have been selected
        for c in ic.choices:
            if not isinstance(c, Separator) and c[1] not in ic.selected_options and not c[2]:
                # add missing ones
                ic.selected_options.append(c[1])
                all_selected = False
        if all_selected:
            ic.selected_options = []

    @kb.add('down', eager=True)
    def move_cursor_down(event):
        def _next():
            ic.pointer_index = ((ic.pointer_index + 1) % ic.line_count)
        _next()
        while isinstance(ic.choices[ic.pointer_index], Separator) or \
                ic.choices[ic.pointer_index][2]:
            _next()

    @kb.add('up', eager=True)
    def move_cursor_up(event):
        def _prev():
            ic.pointer_index = ((ic.pointer_index - 1) % ic.line_count)
        _prev()
        while isinstance(ic.choices[ic.pointer_index], Separator) or \
                ic.choices[ic.pointer_index][2]:
            _prev()

    @kb.add('enter', eager=True)
    def set_answer(event):
        ic.answered = True
        # TODO use validator
        event.app.exit(result=ic.get_selected_values())

    return Application(
        layout=Layout(layout),
        key_bindings=kb,
        mouse_support=True,
        style=style
    )
