# -*- coding: utf-8 -*-

from contextlib import contextmanager
from . import PromptParameterException, prompts
from .prompts import list, confirm, input, password, checkbox, rawlist, expand, editor
from prompt_toolkit.patch_stdout import patch_stdout as pt_patch_stdout
from prompt_toolkit.shortcuts import PromptSession
from prompt_toolkit.application import Application



def prompt(questions, answers=None, **kwargs):
    from . import prompts

    if isinstance(questions, dict):
        questions = [questions]
    answers = answers or {}

    patch_stdout = kwargs.pop('patch_stdout', False)
    return_asyncio_coroutine = kwargs.pop('return_asyncio_coroutine', False)
    true_color = kwargs.pop('true_color', False)
    refresh_interval = kwargs.pop('refresh_interval', 0)
    kbi_msg = kwargs.pop('keyboard_interrupt_msg', 'Cancelled by user')
    raise_kbi = kwargs.pop('raise_keyboard_interrupt', False)

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
            type_ = _kwargs.pop('type')
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

            with pt_patch_stdout() if patch_stdout else _dummy_context_manager():
                result = getattr(prompts, type_).question(message, **_kwargs)


                if isinstance(result, PromptSession):
                    answer = result.prompt()
                elif isinstance(result, Application):
                    answer = result.run()
                else:
                    # assert isinstance(answer, str)
                    answer = result

                # answer = application.run(
                #    return_asyncio_coroutine=return_asyncio_coroutine,
                #    true_color=true_color,
                #    refresh_interval=refresh_interval)

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
            raise ValueError('No question type \'%s\'' % type_)
        except KeyboardInterrupt as exc:
            if raise_kbi:
                raise exc from None
            if kbi_msg:
                print('')
                print(kbi_msg)
                print('')
            return {}
    return answers

@contextmanager
def _dummy_context_manager():
    yield

# TODO:
# Bottom Bar - inquirer.ui.BottomBar
