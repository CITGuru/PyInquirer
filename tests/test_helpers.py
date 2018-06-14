# -*- coding: utf-8 -*-
import textwrap
import pytest

from .helpers import remove_ansi_escape_sequences
from .helpers import create_example_fixture


example_app = create_example_fixture('tests/example_app.py')


def test_remove_ansi_escape_sequences():
    line = 'true\x1b[39;49;00m, \r\n    \x1b[34;01m"favorite"\x1b[39;49;00m: \x1b[33m"smoked bacon"\x1b[39;49;00m\r\n}\r\n\r\n'
    escaped_line = remove_ansi_escape_sequences(line)
    assert escaped_line == 'true,\n    "favorite": "smoked bacon"\n}\n\n'


def test_example_app(example_app):
    # test the helper class plus demonstrate how to use it...
    example_app.expect(textwrap.dedent("""\
        hi, there!
        let's get to know each other better...
        Please enter your name: """))
    example_app.writeline('Stuart')
    assert example_app.readline() == 'Hi Stuart, have a nice day!'
    assert example_app.readline() == 'It was a pleasure talking to you...'


def test_example_app_dialog_style(example_app):
    # test the helper class plus demonstrate how to use it...
    example_app.expect(textwrap.dedent("""\
        hi, there!
        let's get to know each other better...
        Please enter your name: """))
    example_app.writeline('Stuart')
    example_app.expect(textwrap.dedent("""\
        Hi Stuart, have a nice day!
        It was a pleasure talking to you...
        """))


def test_example_app_no_match(example_app):
    # note: the app does not run to its end so the fixture handles cleanup
    with pytest.raises(AssertionError):
        example_app.expect('babadam')


def test_example_app_regex(example_app):
    assert example_app.expect_regex('hi, there!\n.*\nPlease enter your name: ')
    example_app.writeline('Stuart')
    assert example_app.readline() == 'Hi Stuart, have a nice day!'


def test_example_app_regex_no_match(example_app):
    # note: the app does not run to its end so the fixture handles cleanup
    with pytest.raises(AssertionError):
        assert not example_app.expect_regex('babadam')

