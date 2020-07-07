# -*- coding: utf-8 -*-
import textwrap

from .helpers import create_example_fixture


example_app = create_example_fixture('examples/password.py')


def test_password(example_app):
    example_app.expect(textwrap.dedent("""\
        ? Enter your git password"""))
    example_app.writeline('asdf')
    example_app.expect(textwrap.dedent("""\
        ? Enter your git password  ****
        '{\\n    \\x1b[94m"password"\\x1b[39;49;00m: \\x1b[33m"asdf"\\x1b[39;49;00m\\n}\\n'
        """))
