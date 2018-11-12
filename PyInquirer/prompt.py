# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

from prompt_toolkit.shortcuts import run_application

from . import PromptParameterException, prompts
from .prompts import list, confirm, input, password, checkbox, rawlist, expand, editor


def prompt(questions, answers=None, **kwargs):
    if isinstance(questions, dict):
        questions = [questions]
    answers = answers or {}

    patch_stdout = kwargs.pop('patch_stdout', False)
    return_asyncio_coroutine = kwargs.pop('return_asyncio_coroutine', False)
    true_color = kwargs.pop('true_color', False)
    refresh_interval = kwargs.pop('refresh_interval', 0)
    eventloop = kwargs.pop('eventloop', None)
    kbi_msg = kwargs.pop('keyboard_interrupt_msg', 'Cancelled by user')

    for question in questions:
        # import the question
        if 'type' not in question:
            raise PromptParameterException('type')
        if 'name' not in question:
            raise PromptParameterException('name')
        if 'message' not in question:
            raise PromptParameterException('message')
        try:
            choices = question.get('choices')
            if choices is not None and callable(choices):
                question['choices'] = choices(answers)

            _kwargs = {}
            _kwargs.update(kwargs)
            _kwargs.update(question)
            type = _kwargs.pop('type')
            name = _kwargs.pop('name')
            message = _kwargs.pop('message')
            when = _kwargs.pop('when', None)
            filter = _kwargs.pop('filter', None)

            if when:
                # at least a little sanity check!
                if callable(question['when']):
                    try:
                        if not question['when'](answers):
                            continue
                    except Exception as e:
                        raise ValueError(
                            'Problem in \'when\' check of %s question: %s' %
                            (name, e))
                else:
                    raise ValueError('\'when\' needs to be function that ' \
                                     'accepts a dict argument')
            if filter:
                # at least a little sanity check!
                if not callable(question['filter']):
                    raise ValueError('\'filter\' needs to be function that ' \
                                     'accepts an argument')

            if callable(question.get('default')):
                _kwargs['default'] = question['default'](answers)
            
            application = getattr(prompts, type).question(message, **_kwargs)

            answer = run_application(
                application,
                patch_stdout=patch_stdout,
                return_asyncio_coroutine=return_asyncio_coroutine,
                true_color=true_color,
                refresh_interval=refresh_interval,
                eventloop=eventloop)

            if answer is not None:
                if filter:
                    try:
                        answer = question['filter'](answer)
                    except Exception as e:
                        raise ValueError(
                            'Problem processing \'filter\' of %s question: %s' %
                            (name, e))
                answers[name] = answer
        except AttributeError as e:
            print(e)
            raise ValueError('No question type \'%s\'' % type)
        except KeyboardInterrupt:
            print('')
            print(kbi_msg)
            print('')
            return {}
    return answers


# TODO:
# Bottom Bar - inquirer.ui.BottomBar
