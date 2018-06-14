# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import textwrap

from .helpers import keys
from .helpers import create_example_fixture


example_app = create_example_fixture('examples/expand.py')


def test_without_expand(example_app):
    example_app.expect(textwrap.dedent("""\
        ? Conflict on `file.js`:   (yAdxh)
        >> Overwrite this one and all next"""))
    example_app.write('x')
    example_app.expect(textwrap.dedent("""\
        
        Abot                          """))  # only registers changed chars :)
    example_app.write(keys.ENTER)
    example_app.expect(textwrap.dedent("""\
        ? Conflict on `file.js`:   abort
        {
            "overwrite": "abort"
        }

        """))


def test_with_expand(example_app):
    example_app.expect(textwrap.dedent("""\
        ? Conflict on `file.js`:   (yAdxh)
        >> Overwrite this one and all next"""))
    example_app.write('d')
    example_app.write('h')
    example_app.expect(
        "\n" +
        "  y) Ovewrite\n" +
        "  A) Overwrite this one and all next\n" +
        "  d) Show diff\n" +
        "   ---------------\n" +
        "  x) Abort\n" +
        "  h) Help, list all options\n" +
        "  Answer: d")
    example_app.write(keys.ENTER)
    example_app.expect(textwrap.dedent("""\
        ? Conflict on `file.js`:   diff
        {
            "overwrite": "diff"
        }

        """))
