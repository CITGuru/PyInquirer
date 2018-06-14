# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import textwrap

from .helpers import keys
from .helpers import create_example_fixture


example_app = create_example_fixture('examples/rawlist.py')


def test_rawlist(example_app):
    example_app.expect(textwrap.dedent("""\
        ? What do you want to do?
          1) Order a pizza
          2) Make a reservation
           ---------------
          3) Ask opening hours
          4) Talk to the receptionist
          Answer: 1"""))
    example_app.write(keys.ENTER)
    example_app.expect(textwrap.dedent("""\
        ? What do you want to do?  Order a pizza
        ? What size do you need
          1) Jumbo
          2) Large
          3) Standard
          4) Medium
          5) Small
          6) Micro
          Answer: 1"""))
    example_app.write('2')
    # the following line is not necessary but "shows" how this works...
    example_app.expect('\n  1) Jumbo\n  2) Large\n\n\n\n\n2')
    example_app.write(keys.ENTER)
    example_app.expect(textwrap.dedent("""\
        ? What size do you need  Large
        {
            "size": "large",
            "theme": "Order a pizza"
        }
        
        """))
