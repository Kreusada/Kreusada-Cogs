.. _texteditor:

==========
TextEditor
==========

This is the cog guide for the texteditor cog. You will
find detailed docs about usage and commands.

Throughout this documentation, ``[p]`` is considered as your prefix.

------------
Installation
------------

Let's firstly add my repository if you haven't already:

* :code:`[p]repo add kreusada https://github.com/Kreusada/Kreusada-Cogs`

Next, let's download the cog from the repo:

* :code:`[p]cog install kreusada texteditor`

Finally, you can see my end user data statements, cog requirements, and other cog information by using:

* :code:`[p]cog info kreusada texteditor`

.. _texteditor-usage:

-----
Usage
-----

Edit and manipulate with text.


.. _texteditor-commands:

--------
Commands
--------

.. _texteditor-command-editor:

^^^^^^
editor
^^^^^^

**Syntax**

.. code-block:: ini

    [p]editor

**Description**

Base command for editting text.

.. _texteditor-command-editor-alternating:

""""""""""""""""""
editor alternating
""""""""""""""""""

**Syntax**

.. code-block:: ini

    [p]editor alternating <text>

**Description**

Convert the text to alternating case.

.. _texteditor-command-editor-charcount:

""""""""""""""""
editor charcount
""""""""""""""""

**Syntax**

.. code-block:: ini

    [p]editor charcount [include_spaces=True] <text>

**Description**

Count the number of characters appearing in the text.

.. _texteditor-command-editor-lower:

""""""""""""
editor lower
""""""""""""

**Syntax**

.. code-block:: ini

    [p]editor lower <text>

**Description**

Convert the text to lowercase.

.. _texteditor-command-editor-multiply:

"""""""""""""""
editor multiply
"""""""""""""""

**Syntax**

.. code-block:: ini

    [p]editor multiply <multiplier> <text>

**Description**

Multiply the text.

.. _texteditor-command-editor-occurance:

""""""""""""""""
editor occurance
""""""""""""""""

**Syntax**

.. code-block:: ini

    [p]editor occurance <check> <text>

**Description**

Count how many times something appears in the text.

.. _texteditor-command-editor-remove:

"""""""""""""
editor remove
"""""""""""""

**Syntax**

.. code-block:: ini

    [p]editor remove <remove> <text>

**Description**

Remove something from the text.

.. _texteditor-command-editor-replace:

""""""""""""""
editor replace
""""""""""""""

**Syntax**

.. code-block:: ini

    [p]editor replace <text_to_replace> <replacement> <text>

**Description**

Replace certain parts of the text.

.. _texteditor-command-editor-reverse:

""""""""""""""
editor reverse
""""""""""""""

**Syntax**

.. code-block:: ini

    [p]editor reverse <text>

**Description**

Reverse the text.

.. _texteditor-command-editor-shuffle:

""""""""""""""
editor shuffle
""""""""""""""

**Syntax**

.. code-block:: ini

    [p]editor shuffle <text>

.. tip:: Alias: ``editor jumble``

**Description**

Completely shuffle the text.

.. _texteditor-command-editor-snake:

""""""""""""
editor snake
""""""""""""

**Syntax**

.. code-block:: ini

    [p]editor snake <text>

**Description**

Convert all spaces to underscores.

.. _texteditor-command-editor-squash:

"""""""""""""
editor squash
"""""""""""""

**Syntax**

.. code-block:: ini

    [p]editor squash <text>

**Description**

Squash all the words into one.

.. _texteditor-command-editor-title:

""""""""""""
editor title
""""""""""""

**Syntax**

.. code-block:: ini

    [p]editor title <text>

**Description**

Convert the text to titlecase.

.. _texteditor-command-editor-trim:

"""""""""""
editor trim
"""""""""""

**Syntax**

.. code-block:: ini

    [p]editor trim [trimmer= ] <text>

.. tip:: Alias: ``editor strip``

**Description**

Trim the outskirts of the text.

.. _texteditor-command-editor-upper:

""""""""""""
editor upper
""""""""""""

**Syntax**

.. code-block:: ini

    [p]editor upper <text>

**Description**

Convert the text to uppercase.

.. _texteditor-command-editor-wordcount:

""""""""""""""""
editor wordcount
""""""""""""""""

**Syntax**

.. code-block:: ini

    [p]editor wordcount <text>

**Description**

Count the number of words appearing in the text.

---------------
Receive Support
---------------

Feel free to ping me at the `Red Cog Support Server <https://discord.gg/GET4DVk>`_ in :code:`#support_kreusada-cogs`.
