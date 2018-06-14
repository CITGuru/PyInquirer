# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import textwrap

from .helpers import keys, create_example_fixture


example_app = create_example_fixture('examples/hierarchical.py')


def test_hierarchical(example_app):
    example_app.expect(textwrap.dedent("""\
        You find yourself in a small room, there is a door in front of you.
        ? Which direction would you like to go?  (Use arrow keys)
         ❯ Forward
           Right
           Left
           Back"""))
    example_app.write(keys.DOWN)
    example_app.write(keys.ENTER)
    example_app.expect(textwrap.dedent("""\
        ? Which direction would you like to go?  Right
        You cannot go that way. Try again
        ? Which direction would you like to go?  (Use arrow keys)
         ❯ Forward
           Right
           Left
           Back"""))
    example_app.write(keys.ENTER)
    example_app.expect(textwrap.dedent("""\
        ? Which direction would you like to go?  Forward
        You find yourself in a forest
        There is a wolf in front of you; a friendly looking dwarf to the right and an impasse to the left.
        ? Which direction would you like to go?  (Use arrow keys)
         ❯ Forward
           Right
           Left
           Back"""))
    example_app.write(keys.DOWN)
    example_app.write(keys.ENTER)
    example_app.expect(textwrap.dedent("""\
        ? Which direction would you like to go?  Right
        You befriend the dwarf
        He helps you kill the wolf. You can now move forward
        ? Which direction would you like to go?  (Use arrow keys)
         ❯ Forward
           Right
           Left
           Back"""))
    example_app.write(keys.ENTER)
    example_app.expect(textwrap.dedent("""\
        ? Which direction would you like to go?  Forward
        You find a painted wooden sign that says:
         ____  _____  ____  _____
        (_  _)(  _  )(  _ \(  _  )
          )(   )(_)(  )(_) ))(_)(
         (__) (_____)(____/(_____)
        
        """))
