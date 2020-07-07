# -*- coding: utf-8 -*-
import textwrap

from .helpers import keys
from .helpers import create_example_fixture


example_app = create_example_fixture('examples/when.py')


def test_when_bacon(example_app):
    example_app.expect('? Do you like bacon?  (Y/n)')
    example_app.write(keys.ENTER)

    example_app.expect(textwrap.dedent("""\
        ? Do you like bacon?  Yes
        ? Bacon lover, what is your favorite type of bacon?  """))
    example_app.writeline('smoked bacon')
    example_app.expect(textwrap.dedent("""\
        ? Bacon lover, what is your favorite type of bacon?  smoked bacon
        ('{\\n'
         '    \\x1b[94m"bacon"\\x1b[39;49;00m: \\x1b[34mtrue\\x1b[39;49;00m,\\n'
         '    \\x1b[94m"favorite"\\x1b[39;49;00m: \\x1b[33m"smoked bacon"\\x1b[39;49;00m\\n'
         '}\\n')
        """))


def test_when_pizza(example_app):
    example_app.expect('? Do you like bacon?  (Y/n)')
    example_app.write('n')

    example_app.expect(textwrap.dedent("""\
        ? Do you like bacon?  No
        ? Ok... Do you like pizza?  (y/N)"""))
    example_app.write('y')

    example_app.expect(textwrap.dedent("""\
        ? Ok... Do you like pizza?  Yes
        ? Whew! What is your favorite type of pizza?  """))
    example_app.writeline('Toscana')

    example_app.expect(textwrap.dedent("""\
        ? Whew! What is your favorite type of pizza?  Toscana
        ('{\\n'
         '    \\x1b[94m"bacon"\\x1b[39;49;00m: \\x1b[34mfalse\\x1b[39;49;00m,\\n'
         '    \\x1b[94m"favorite"\\x1b[39;49;00m: \\x1b[33m"Toscana"\\x1b[39;49;00m,\\n'
         '    \\x1b[94m"pizza"\\x1b[39;49;00m: \\x1b[34mtrue\\x1b[39;49;00m\\n'
         '}\\n')
        """))


def test_when_no_thanks(example_app):
    example_app.expect('? Do you like bacon?  (Y/n)')
    example_app.write('n')

    example_app.expect(textwrap.dedent("""\
        ? Do you like bacon?  No
        ? Ok... Do you like pizza?  (y/N)"""))
    example_app.write('n')

    example_app.expect(textwrap.dedent("""\
        ? Ok... Do you like pizza?  No
        ('{\\n'
         '    \\x1b[94m"bacon"\\x1b[39;49;00m: \\x1b[34mfalse\\x1b[39;49;00m,\\n'
         '    \\x1b[94m"pizza"\\x1b[39;49;00m: \\x1b[34mfalse\\x1b[39;49;00m\\n'
         '}\\n')
        """))
