# -*- coding: utf-8 -*-
"""
`editor` type question
"""
from __future__ import print_function, unicode_literals
import os
import sys
from prompt_toolkit.token import Token
from prompt_toolkit.shortcuts import create_prompt_application
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.layout.lexers import SimpleLexer

from .common import default_style


# use std prompt-toolkit control

WIN = sys.platform.startswith('win')

class EditorArgumentsError(Exception):
    pass

class Editor(object):

    def __init__(self, editor=None, env=None, require_save=True, extension='.txt'):
        self.editor = editor
        self.env = env
        self.require_save = require_save
        self.extension = extension

    def get_editor(self):
        if self.editor is not None and self.editor.lower() != "default":
            return self.editor
        for key in 'VISUAL', 'EDITOR':
            rv = os.environ.get(key)
            if rv:
                return rv
        if WIN:
            return 'notepad'
        for editor in 'vim', 'nano':
            if os.system('which %s >/dev/null 2>&1' % editor) == 0:
                return editor
        return 'vi'

    def edit_file(self, filename):
        import subprocess
        editor = self.get_editor()
        if self.env:
            environ = os.environ.copy()
            environ.update(self.env)
        else:
            environ = None
        try:
            c = subprocess.Popen('%s "%s"' % (editor, filename),
                                 env=environ, shell=True)
            exit_code = c.wait()
            if exit_code != 0:
                raise Exception('%s: Editing failed!' % editor)
        except OSError as e:
            raise Exception('%s: Editing failed: %s' % (editor, e))

    def edit(self, text):
        import tempfile

        text = text or ''
        if text and not text.endswith('\n'):
            text += '\n'

        fd, name = tempfile.mkstemp(prefix='editor-', suffix=self.extension)
        try:
            if WIN:
                encoding = 'utf-8-sig'
                text = text.replace('\n', '\r\n')
            else:
                encoding = 'utf-8'
            text = text.encode(encoding)

            f = os.fdopen(fd, 'wb')
            f.write(text)
            f.close()
            timestamp = os.path.getmtime(name)

            self.edit_file(name)

            if self.require_save \
               and os.path.getmtime(name) == timestamp:
                return None

            f = open(name, 'rb')
            try:
                rv = f.read()
            finally:
                f.close()
            return rv.decode('utf-8-sig').replace('\r\n', '\n')
        finally:
            os.unlink(name)

def edit(text=None, editor=None, env=None, require_save=True,
         extension='.txt', filename=None):
    r"""Edits the given text in the defined editor.  If an editor is given
    (should be the full path to the executable but the regular operating
    system search path is used for finding the executable) it overrides
    the detected editor.  Optionally, some environment variables can be
    used.  If the editor is closed without changes, `None` is returned.  In
    case a file is edited directly the return value is always `None` and
    `require_save` and `extension` are ignored.

    If the editor cannot be opened a :exc:`UsageError` is raised.

    Note for Windows: to simplify cross-platform usage, the newlines are
    automatically converted from POSIX to Windows and vice versa.  As such,
    the message here will have ``\n`` as newline markers.

    :param text: the text to edit.
    :param editor: optionally the editor to use.  Defaults to automatic
                   detection.
    :param env: environment variables to forward to the editor.
    :param require_save: if this is true, then not saving in the editor
                         will make the return value become `None`.
    :param extension: the extension to tell the editor about.  This defaults
                      to `.txt` but changing this might change syntax
                      highlighting.
    :param filename: if provided it will edit this file instead of the
                     provided text contents.  It will not use a temporary
                     file as an indirection in that case.
    """

    editor = Editor(editor=editor, env=env, require_save=require_save,
                    extension=extension)
    if filename is None:
        return editor.edit(text)
    editor.edit_file(filename)

def question(message, **kwargs):
    default = kwargs.pop('default', '')
    eargs = kwargs.pop('eargs', {})
    validate_prompt = kwargs.pop('validate', None)
    if validate_prompt:
        if issubclass(validate_prompt, Validator):
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

    for k, v in eargs.items():
        if v == "" or v == " ":
            raise EditorArgumentsError(
                "Args '{}' value should not be empty".format(k)
            )
    
    editor = eargs.get("editor", None)
    ext = eargs.get("ext", ".txt")
    env = eargs.get("env", None)
    text = default
    filename = eargs.get("filename", None)
    multiline = True if not editor else False
    save = eargs.get("save", None)

    if editor:
        _text = edit(
            editor=editor, 
            extension=ext,
            text=text,
            env=env,
            filename=filename,
            require_save=save
        )
        if filename:
            default = filename
        else:
            default = _text

    # TODO style defaults on detail level
    kwargs['style'] = kwargs.pop('style', default_style)
    qmark = kwargs.pop('qmark', '?')
    
    def _get_prompt_tokens(cli):
        return [
            (Token.QuestionMark, qmark),
            (Token.Question, ' %s  ' % message)
        ]

    return create_prompt_application(
        get_prompt_tokens=_get_prompt_tokens,
        lexer=SimpleLexer(Token.Answer),
        default=default,
        multiline=multiline,
        **kwargs
    )
