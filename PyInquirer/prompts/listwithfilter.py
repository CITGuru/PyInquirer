# -*- coding: utf-8 -*-
"""
`list` type question

Complete re-write with filter support. Taken from:
https://github.com/gbataille/password-organizer/blob/master/password_organizer/cli_menu/prompts/listmenu.py
"""
from dataclasses import dataclass
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.filters import Condition, IsDone
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.controls import (
    FormattedTextControl, GetLinePrefixCallable, UIContent, UIControl
)
from prompt_toolkit.layout.containers import ConditionalContainer, HSplit, Window
from prompt_toolkit.layout.dimension import LayoutDimension as D
import string
from typing import Generic, List, Optional, TypeVar
from ..separator import Separator
from .common import default_style



class ChoicesControl(UIControl):
    """
    Menu to display some textual choices.
    Provide a search feature by just typing the start of the entry desired
    """
    def __init__(self, choices, **kwargs):
        # Selection to keep consistent
        self._selected_choice = None
        self._selected_index: int = -1

        self._answered = False
        self._search_string: Optional[str] = None
        self._choices = choices
        self._cached_choices = None

        self._init_choices(default=kwargs.pop('default'))
        super().__init__(**kwargs)

    def _init_choices(self, default=None):
        if default is not None and self._find_choice(default) is None:
            raise ValueError(f"Default value {default} is not part of the given choices")
        self._compute_available_choices(default=default)

    @property
    def is_answered(self) -> bool:
        return self._answered

    @is_answered.setter
    def is_answered(self, value: bool) -> None:
        self._answered = value

    def _get_available_choices(self) -> None:
        if self._cached_choices is None:
            self._compute_available_choices()

        return self._cached_choices or []


    def _compute_available_choices(self, default = None) -> None:
        self._cached_choices = []

        for choice in self._choices:
            if self._search_string:
                if isinstance(choice, Separator):
                    self._cached_choices.append(choice)
                elif isinstance(choice, str):
                    if self._search_string.lower() in choice.lower():
                        self._cached_choices.append(choice)
                else:
                    if self._search_string.lower() in choice.get('name').lower():
                        self._cached_choices.append(choice)
            else:
                self._cached_choices.append(choice)

        if self._cached_choices == []:
            self._selected_choice = None
            self._selected_index = -1
        else:
            if default is not None:
                self._selected_choice = self._find_choice(default)
                self._selected_index = self._cached_choices.index(self._selected_choice)

            if self._selected_choice not in self._cached_choices:
                self._selected_choice = self._cached_choices[0]
                self._selected_index = 0
                if isinstance(self._selected_choice, str):
                    pass
                elif isinstance(self._selected_choice, Separator):
                    self.select_next_choice()
                else:
                    while self._selected_choice.get('disabled', False):
                        self.select_next_choice()

    def _find_choice(self, value):
        for choice in self._choices:
            if isinstance(choice, Separator):
                continue
            elif isinstance(choice, str):
                if value == choice:
                    return choice
            else:
                if value == choice.get('value'):
                    return choice

    def _reset_cached_choices(self) -> None:
        self._cached_choices = None

    def get_selection(self):
        return self._selected_choice

    def select_next_choice(self) -> None:
        if not self._cached_choices or self._selected_choice is None:
            return

        def _next():
            self._selected_index += 1
            self._selected_choice = self._cached_choices[self._selected_index % self.choice_count]

        _next()
        if isinstance(self._selected_choice, str):
            pass
        elif isinstance(self._selected_choice, Separator):
            _next()
        else:
            while isinstance(self._selected_choice, dict) and self._selected_choice.get('disabled', False):
                _next()


    def select_previous_choice(self) -> None:
        if not self._cached_choices or self._selected_choice is None:
            return

        def _prev():
            self._selected_index -= 1
            self._selected_choice = self._cached_choices[self._selected_index % self.choice_count]

        _prev()
        if isinstance(self._selected_choice, str):
            pass
        elif isinstance(self._selected_choice, Separator):
            _prev()
        else:
            while isinstance(self._selected_choice, dict) and self._selected_choice.get('disabled', False):
                _prev()

    def preferred_width(self, max_available_width: int) -> int:
        max_elem_width = max(list(map(lambda x: x.display_length, self._choices)))
        return min(max_elem_width, max_available_width)

    def preferred_height(
        self,
        width: int,
        max_available_height: int,
        wrap_lines: bool,
        get_line_prefix: Optional[GetLinePrefixCallable],
    ) -> Optional[int]:
        return self.choice_count

    def create_content(self, width: int, height: int) -> UIContent:

        def _get_line_tokens(line_number):
            choice = self._get_available_choices()[line_number]
            tokens = []

            selected = (choice == self.get_selection())
            if isinstance(choice, Separator):
                tokens.append(('class:separator', '  %s\n' % choice))
            else:
                tokens.append(('class:pointer' if selected else '', ' \u276f ' if selected
                    else '   '))
                if selected:
                    tokens.append(('[SetCursorPosition]', ''))
                if isinstance(choice, str):
                    tokens.append(('class:selected' if selected else '', str(choice)))
                else:
                    if choice.get('disabled', False):
                        token_text = choice.get('name')
                        if isinstance(choice.get('disabled'), str):
                            token_text += f' ({choice.get("disabled")})'
                        tokens.append(('class:selected' if selected else 'class:disabled', token_text))
                    else:
                        tokens.append(('class:selected' if selected else '', str(choice.get('name', choice))))

            return tokens

        return UIContent(
            get_line=_get_line_tokens,
            line_count=self.choice_count,
        )

    @property
    def choice_count(self):
        return len(self._get_available_choices())

    def get_search_string_tokens(self):
        if self._search_string is None:
            return None

        return [
            ('', '\n'),
            ('class:question-mark', '/ '),
            ('class:search', self._search_string),
            ('class:question-mark', '...'),
        ]

    def append_to_search_string(self, char: str) -> None:
        """ Appends a character to the search string """
        if self._search_string is None:
            self._search_string = ''
        self._search_string += char
        self._reset_cached_choices()

    def remove_last_char_from_search_string(self) -> None:
        """ Remove the last character from the search string (~backspace) """
        if self._search_string and len(self._search_string) > 1:
            self._search_string = self._search_string[:-1]
        else:
            self._search_string = None
        self._reset_cached_choices()

    def reset_search_string(self) -> None:
        self._search_string = None


def question(message, **kwargs):
    """
    Builds a `prompt-toolkit` Application that display a list of choices (ChoiceControl) along with
    search features and key bindings

    Paramaters
    ==========
    kwargs: Dict[Any, Any]
        Any additional arguments that a prompt_toolkit.application.Application can take. Passed
        as-is
    """
    # TODO disabled, dict choices
    if not 'choices' in kwargs:
        raise PromptParameterException('choices')

    choices = kwargs.pop('choices', None)
    default = kwargs.pop('default', None)
    key_bindings = kwargs.pop('key_bindings', None)
    qmark = kwargs.pop('qmark', '?')
    # TODO style defaults on detail level
    style = kwargs.pop('style', default_style)

    if key_bindings is None:
        key_bindings = KeyBindings()

    choices_control = ChoicesControl(choices, default=default)

    def get_prompt_tokens():
        tokens = []

        tokens.append(('class:question-mark', qmark))
        tokens.append(('class:question', ' %s ' % message))
        if choices_control.is_answered:
            if isinstance(choices_control.get_selection(), str):
                tokens.append(('class:answer', ' ' + choices_control.get_selection()))
            else:
                tokens.append(('class:answer', ' ' + choices_control.get_selection().get('name')))
        else:
            tokens.append(('class:instruction', ' (Use arrow keys or type to filter)'))
        return tokens

    @Condition
    def has_search_string():
        return choices_control.get_search_string_tokens is not None

    @key_bindings.add(Keys.ControlQ, eager=True)
    def exit_menu(event):
        event.app.exit(exception=KeyboardInterrupt())

    if not key_bindings.get_bindings_for_keys((Keys.ControlC,)):
        key_bindings.add(Keys.ControlC, eager=True)(exit_menu)

    @key_bindings.add(Keys.Down, eager=True)
    def move_cursor_down(_event):        # pylint:disable=unused-variable
        choices_control.select_next_choice()

    @key_bindings.add(Keys.Up, eager=True)
    def move_cursor_up(_event):        # pylint:disable=unused-variable
        choices_control.select_previous_choice()

    @key_bindings.add(Keys.Enter, eager=True)
    def set_answer(event):        # pylint:disable=unused-variable
        choices_control.is_answered = True
        choices_control.reset_search_string()
        if isinstance(choices_control.get_selection(), str):
            event.app.exit(result=choices_control.get_selection())
        else:
            event.app.exit(result=choices_control.get_selection().get('value'))

    def search_filter(event):
        choices_control.append_to_search_string(event.key_sequence[0].key)

    for character in string.printable:
        key_bindings.add(character, eager=True)(search_filter)

    @key_bindings.add(Keys.Backspace, eager=True)
    def delete_from_search_filter(_event):        # pylint:disable=unused-variable
        choices_control.remove_last_char_from_search_string()

    layout = Layout(
        HSplit([
            # Question
            Window(
                height=D.exact(1),
                content=FormattedTextControl(get_prompt_tokens),
                always_hide_cursor=True,
            ),
            # Choices
            ConditionalContainer(
                Window(choices_control),
                filter=~IsDone()        # pylint:disable=invalid-unary-operand-type
            ),
            # Searched string
            ConditionalContainer(
                Window(
                    height=D.exact(2),
                    content=FormattedTextControl(choices_control.get_search_string_tokens)
                ),
                filter=has_search_string & ~IsDone()    # pylint:disable=invalid-unary-operand-type
            ),
        ])
    )

    return Application(
        layout=layout,
        key_bindings=key_bindings,
        mouse_support=False,
        style=style
    )
