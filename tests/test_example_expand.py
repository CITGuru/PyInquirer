# -*- coding: utf-8 -*-
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
        '{\\n    \\x1b[94m"overwrite"\\x1b[39;49;00m: \\x1b[33m"abort"\\x1b[39;49;00m\\n}\\n'
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
        '{\\n    \\x1b[94m"overwrite"\\x1b[39;49;00m: \\x1b[33m"diff"\\x1b[39;49;00m\\n}\\n'
        """))
