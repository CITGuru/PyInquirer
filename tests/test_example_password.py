# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import textwrap

from .helpers import create_example_fixture


example_app = create_example_fixture('examples/password.py')


def test_password(example_app):
    example_app.expect(textwrap.dedent("""\
        ? Enter your git password  """))
    example_app.writeline('asdf')
    example_app.expect(textwrap.dedent("""\
        ? Enter your git password  ****
        {
            "password": "asdf"
        }
        
        """))
