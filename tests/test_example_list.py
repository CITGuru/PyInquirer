# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import textwrap

from .helpers import keys
from .helpers import create_example_fixture


example_app = create_example_fixture('examples/list.py')


def test_list(example_app):
    example_app.expect(textwrap.dedent("""\
        ? What do you want to do?  (Use arrow keys)
         ❯ Order a pizza
           Make a reservation
           ---------------
           Ask for opening hours
           - Contact support (Unavailable at this time)
           Talk to the receptionist"""))
    example_app.write(keys.ENTER)
    example_app.expect(textwrap.dedent("""\
        ? What do you want to do?  Order a pizza
        ? What size do you need?  (Use arrow keys)
         ❯ Jumbo
           Large
           Standard
           Medium
           Small
           Micro"""))
    example_app.write(keys.ENTER)
    example_app.expect(textwrap.dedent("""\
        ? What size do you need?  Jumbo
        ? Which vehicle you want to use for delivery?  (Use arrow keys)
         ❯ bike
           car
           truck
           helicopter"""))
    example_app.write(keys.ENTER)
    example_app.expect(textwrap.dedent("""\
        ? Which vehicle you want to use for delivery?  bike
        {'delivery': 'bike', 'size': 'jumbo', 'theme': 'Order a pizza'}
        """))
