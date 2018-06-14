# -*- coding: utf-8 -*-
from PyInquirer.prompts import list  # this import is necessary!
from .helpers import feed_app_with_input, keys


def test_select_first_choice():
    message = 'Foo message'
    name = 'Bar variable'
    kwargs = {
        'choices': ['foo', 'bar', 'bazz']
    }
    text = keys.ENTER

    result, cli = feed_app_with_input('list', message, text, **kwargs)
    assert result == 'foo'


def test_select_second_choice():
    message = 'Foo message'
    name = 'Bar variable'
    kwargs = {
        'choices': ['foo', 'bar', 'bazz']
    }
    text = keys.DOWN + keys.ENTER

    result, cli = feed_app_with_input('list', message, text, **kwargs)
    assert result == 'bar'


def test_select_third_choice():
    message = 'Foo message'
    name = 'Bar variable'
    kwargs = {
        'choices': ['foo', 'bar', 'bazz']
    }
    text = keys.DOWN + keys.DOWN + keys.ENTER

    result, cli = feed_app_with_input('list', message, text, **kwargs)
    assert result == 'bazz'


def test_cycle_to_first_choice():
    message = 'Foo message'
    name = 'Bar variable'
    kwargs = {
        'choices': ['foo', 'bar', 'bazz']
    }
    text = keys.DOWN + keys.DOWN + keys.DOWN + keys.ENTER

    result, cli = feed_app_with_input('list', message, text, **kwargs)
    assert result == 'foo'


def test_cycle_backwards():
    message = 'Foo message'
    name = 'Bar variable'
    kwargs = {
        'choices': ['foo', 'bar', 'bazz']
    }
    text = keys.UP + keys.ENTER

    result, cli = feed_app_with_input('list', message, text, **kwargs)
    assert result == 'bazz'


# TODO number shortcuts + tests from Inquirer.js
