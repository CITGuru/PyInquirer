# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import textwrap

from .helpers import create_example_fixture, keys


example_app = create_example_fixture('examples/pizza.py')


def test_pizza(example_app):
    example_app.expect(textwrap.dedent("""\
        Hi, welcome to Python Pizza
        ? Is this for delivery?  (y/N)"""))
    example_app.write('n')
    example_app.expect(textwrap.dedent("""\
        ? Is this for delivery?  No
        ? What's your phone number?  """))
    example_app.writeline('1111111111')
    example_app.expect(textwrap.dedent("""\
        ? What's your phone number?  1111111111
        ? What size do you need?  (Use arrow keys)
         ❯ Large
           Medium
           Small"""))
    example_app.write(keys.ENTER)
    example_app.expect(textwrap.dedent("""\
        ? What size do you need?  Large
        ? How many do you need?  """))
    example_app.writeline('2')
    example_app.expect(textwrap.dedent("""\
        ? How many do you need?  2
        ? What about the toppings?  (pawh)
        >> Pepperoni and cheese"""))
    example_app.write(keys.ENTER)
    example_app.expect(textwrap.dedent("""\
        ? What about the toppings?  PepperoniCheese
        ? You also get a free 2L beverage
          1) Pepsi
          2) 7up
          3) Coke
          Answer: 1"""))
    example_app.write(keys.ENTER)
    example_app.expect(textwrap.dedent("""\
        ? You also get a free 2L beverage  Pepsi
        ? Any comments on your purchase experience?  Nope, all good!"""))
    example_app.write(keys.ENTER)
    example_app.expect(textwrap.dedent("""\
        ? Any comments on your purchase experience?  Nope, all good!
        Order receipt:
        {
            "beverage": "Pepsi",
            "comments": "Nope, all good!",
            "phone": "1111111111",
            "quantity": 2,
            "size": "large",
            "toBeDelivered": false,
            "toppings": "PepperoniCheese"
        }
        
        """))
