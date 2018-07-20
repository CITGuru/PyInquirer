PythonInquirer
==============

A collection of common interactive command line user interfaces. It is
originally called `whaaaaaat <https://github.com/finklabs/whaaaaat>`__
created by **finklabs**, but due to bad naming and in need of fixes, I
decided to rename and apply some necessary fixes on it. The reason is
because I needed it for a tool that can be install through PyPI. I need
to rewrite it for my own need. But don't worry any new fix on the main
Repo, will be added to it if needed. Lastly, I am currently working on
the author's TODO.

Table of Contents
-----------------

1. `Documentation <#documentation>`__

   1. `Installation <#installation>`__
   2. `Examples <#examples>`__
   3. `Quickstart <#quickstart>`__
   4. `Question Types <#types>`__
   5. `Question Properties <#properties>`__
   6. `User Interfaces and Styles <#styles>`__

2. `Windows Platform <#windows>`__
3. `Support <#support>`__
4. `Contribution <#contribution>`__
5. `Acknowledgments <#acknowledgements>`__
6. `License <#license>`__

Goal and Philosophy
-------------------

**``PyInquirer``** strives to be an easily embeddable and beautiful
command line interface for `Python <https://python.org/>`__.
**``PyInquirer``** wants to make it easy for existing Inquirer.js users
to write immersive command line applications in Python. We are convinced
that its feature-set is the most complete for building immersive CLI
applications. We also hope that **``PyInquirer``** proves itself useful
to Python users.

**``PyInquirer``** should ease the process of - providing *error
feedback* - *asking questions* - *parsing* input - *validating* answers
- managing *hierarchical prompts*

**Note:** **``PyInquirer``** provides the user interface and the inquiry
session flow. >

Documentation
-------------

Installation
~~~~~~~~~~~~

Like most Python packages PyInquirer is available on `PyPi <TODO>`__.
Simply use pip to install the PyInquirer package

.. code:: shell

    pip install PyInquirer

In case you encounter any prompt\_toolkit error, that means you've the
wrong prompt\_toolkit version.

You can correct that by doing

.. code:: shell

    pip install prompt_toolkit==1.0.14

or download the wheel file from here:

.. code:: shell

    https://pypi.org/project/prompt_toolkit/1.0.14/#files

Quickstart
~~~~~~~~~~

Like Inquirer.js, using inquirer is structured into two simple steps:

-  you define a **list of questions** and hand them to **prompt**
-  promt returns a **list of answers**

.. code:: python

    from __future__ import print_function, unicode_literals
    from PyInquirer import prompt, print_json

    questions = [
        {
            'type': 'input',
            'name': 'first_name',
            'message': 'What\'s your first name',
        }
    ]

    answers = prompt(questions)
    print_json(answers)  # use the answers as input for your app

A good starting point from here is probably the examples section.

Examples
~~~~~~~~

Most of the examples intend to demonstrate a single question type or
feature:

-  bottom-bar.py
-  expand.py
-  list.py
-  password.py
-  when.py
-  checkbox.py
-  hierarchical.py
-  pizza.py - demonstrate using different question types
-  editor.py
-  input.py
-  rawlist.py

Question Types
~~~~~~~~~~~~~~

``questions`` is a list of questions. Each question has a type.

List - ``{type: 'list'}``
^^^^^^^^^^^^^^^^^^^^^^^^^

Take ``type``, ``name``, ``message``, ``choices``\ [, ``default``,
``filter``] properties. (Note that default must be the choice ``index``
in the array or a choice ``value``)

|List prompt| s ---

Raw List - ``{type: 'rawlist'}``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Take ``type``, ``name``, ``message``, ``choices``\ [, ``default``,
``filter``] properties. (Note that default must the choice ``index`` in
the array)

.. figure:: https://raw.githubusercontent.com/citguru/PyInquirer/master/docs/images/raw-list.png
   :alt: Raw list prompt

   Raw list prompt

--------------

Expand - ``{type: 'expand'}``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Take ``type``, ``name``, ``message``, ``choices``\ [, ``default``]
properties. (Note that default must be the choice ``index`` in the
array. If ``default`` key not provided, then ``help`` will be used as
default choice)

Note that the ``choices`` object will take an extra parameter called
``key`` for the ``expand`` prompt. This parameter must be a single
(lowercased) character. The ``h`` option is added by the prompt and
shouldn't be defined by the user.

See ``examples/expand.py`` for a running example.

|Expand prompt closed| |Expand prompt expanded|

--------------

Checkbox - ``{type: 'checkbox'}``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Take ``type``, ``name``, ``message``, ``choices``\ [, ``filter``,
``validate``, ``default``] properties. ``default`` is expected to be an
Array of the checked choices value.

Choices marked as ``{checked: true}`` will be checked by default.

Choices whose property ``disabled`` is truthy will be unselectable. If
``disabled`` is a string, then the string will be outputted next to the
disabled choice, otherwise it'll default to ``"Disabled"``. The
``disabled`` property can also be a synchronous function receiving the
current answers as argument and returning a boolean or a string.

.. figure:: https://raw.githubusercontent.com/citguru/PyInquirer/master/docs/images/checkbox-prompt.png
   :alt: Checkbox prompt

   Checkbox prompt

--------------

Confirm - ``{type: 'confirm'}``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Take ``type``, ``name``, ``message``\ [, ``default``] properties.
``default`` is expected to be a boolean if used.

.. figure:: https://raw.githubusercontent.com/citguru/PyInquirer/master/docs/images/confirm-prompt.png
   :alt: Confirm prompt

   Confirm prompt

--------------

Input - ``{type: 'input'}``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Take ``type``, ``name``, ``message``\ [, ``default``, ``filter``,
``validate``] properties.

.. figure:: https://raw.githubusercontent.com/citguru/PyInquirer/master/docs/images/input-prompt.png
   :alt: Input prompt

   Input prompt

--------------

Password - ``{type: 'password'}``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Take ``type``, ``name``, ``message``\ [, ``default``, ``filter``,
``validate``] properties.

.. figure:: https://raw.githubusercontent.com/citguru/PyInquirer/master/docs/images/password-prompt.png
   :alt: Password prompt

   Password prompt

--------------

Editor - ``{type: 'editor'}``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Take ``type``, ``name``, ``message``\ [, ``default``, ``filter``,
``validate``] properties

Launches an instance of the users preferred editor on a temporary file.
Once the user exits their editor, the contents of the temporary file are
read in as the result. The editor to use is determined by reading the
:math:`VISUAL or `\ EDITOR environment variables. If neither of those
are present, notepad (on Windows) or vim (Linux or Mac) is used.

Question Properties
~~~~~~~~~~~~~~~~~~~

A question is a dictionary containing question related values:

-  type: (String) Type of the prompt. Defaults: input - Possible values:
   input, confirm, list, rawlist, expand, checkbox, password, editor
-  name: (String) The name to use when storing the answer in the answers
   hash. If the name contains periods, it will define a path in the
   answers hash.
-  message: (String\|Function) The question to print. If defined as a
   function, the first parameter will be the current inquirer session
   answers.
-  default: (String\|Number\|Array\|Function) Default value(s) to use if
   nothing is entered, or a function that returns the default value(s).
   If defined as a function, the first parameter will be the current
   inquirer session answers.
-  choices: (Array\|Function) Choices array or a function returning a
   choices array. If defined as a function, the first parameter will be
   the current inquirer session answers. Array values can be simple
   strings, or objects containing a name (to display in list), a value
   (to save in the answers hash) and a short (to display after
   selection) properties. The choices array can also contain a
   Separator.
-  validate: (Function) Receive the user input and should return true if
   the value is valid, and an error message (String) otherwise. If false
   is returned, a default error message is provided.
-  filter: (Function) Receive the user input and return the filtered
   value to be used inside the program. The value returned will be added
   to the Answers hash.
-  when: (Function, Boolean) Receive the current user answers hash and
   should return true or false depending on whether or not this question
   should be asked. The value can also be a simple boolean.
-  pageSize: (Number) Change the number of lines that will be rendered
   when using list, rawList, expand or checkbox.

User Interfaces and Styles
~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO

Windows Platform
----------------

**``PyInquirer``** is build on prompt\_toolkit which is cross platform,
and everything that you build on top should run fine on both Unix and
Windows systems. On Windows, it uses a different event loop
(WaitForMultipleObjects instead of select), and another input and output
system. (Win32 APIs instead of pseudo-terminals and VT100.)

It's worth noting that the implementation is a "best effort of what is
possible". Both Unix and Windows terminals have their limitations. But
in general, the Unix experience will still be a little better.

For Windows, it's recommended to use either cmder or conemu.

Support
-------

Most of the questions are probably related to using a question type or
feature. Please lookup and study the appropriate examples.

Issue on Github TODO link

For many issues like for example common Python programming issues
stackoverflow might be a good place to search for an answer. TODO link

 ## Contribution

Yes, you can contribute to this.

License
-------

Since I am not the owner, it all goes to Finklab

Copyright (c) 2016-2017 Mark Fink (twitter: @markfink)

Copyright (c) 2018 Oyetoke Toby (twitter: @oyetokeT)

Licensed under the MIT license.

.. |List prompt| image:: https://raw.githubusercontent.com/citguru/PyInquirer/master/docs/images/input-prompt.png
.. |Expand prompt closed| image:: https://raw.githubusercontent.com/citguru/PyInquirer/master/docs/images/expand-prompt-1.png
.. |Expand prompt expanded| image:: https://raw.githubusercontent.com/citguru/PyInquirer/master/docs/images/expand-prompt-2.png
