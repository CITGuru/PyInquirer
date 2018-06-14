# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import textwrap

from .helpers import create_example_fixture, keys


example_app = create_example_fixture('examples/checkbox.py')


def test_checkbox(example_app):
    example_app.expect(textwrap.dedent("""\
        ? Select toppings  (<up>, <down> to move, <space> to select, <a> to toggle, <i>
          = The Meats =
         ❯○ Ham
          ○ Ground Meat
          ○ Bacon
          = The Cheeses =
          ● Mozzarella
          ○ Cheddar
          ○ Parmesan
          = The usual =
          ○ Mushroom
          ○ Tomato
          ○ Pepperoni
          = The extras =
          ○ Pineapple
          - Olives (out of stock)
          ○ Extra cheese"""))
    example_app.write(' ')
    example_app.expect('\n\n● ')
    example_app.write(keys.ENTER)
    example_app.expect(textwrap.dedent("""\
        ? Select toppings  done (2 selections)
        {
            "toppings": [
                "Ham",
                "Mozzarella"
            ]
        }

        """))
