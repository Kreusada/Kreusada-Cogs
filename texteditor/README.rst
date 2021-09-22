.. _texteditor:

==========
TextEditor
==========

This is the cog guide for the 'TextEditor' cog. This guide
contains the collection of commands which you can use in the cog.

Through this guide, ``[p]`` will always represent your prefix. Replace
``[p]`` with your own prefix when you use these commands in Discord.

.. note::

    This guide was last updated for version 3.0.1. Ensure
    that you are up to date by running ``[p]cog update texteditor``.

    If there is something missing, or something that needs improving
    in this documentation, feel free to create an issue `here <https://github.com/Kreusada/Kreusada-Cogs/issues>`_.

    This documentation is auto-generated everytime this cog receives an update.

--------------
About this cog
--------------

Edit and manipulate with text.

--------
Commands
--------

Here are all the commands included in this cog (16):

* ``[p]editor``
 Base command for editting text.
* ``[p]editor alternating <text>``
 Convert the text to alternating case.
* ``[p]editor charcount [include_spaces=True] <text>``
 Count the number of characters appearing in the text.
* ``[p]editor lower <text>``
 Convert the text to lowercase.
* ``[p]editor multiply <multiplier> <text>``
 Multiply the text.
* ``[p]editor occurance <check> <text>``
 Count how many times something appears in the text.
* ``[p]editor remove <remove> <text>``
 Remove something from the text.
* ``[p]editor replace <text_to_replace> <replacement> <text>``
 Replace certain parts of the text.
* ``[p]editor reverse <text>``
 Reverse the text.
* ``[p]editor shuffle <text>``
 Completely shuffle the text.
* ``[p]editor snake <text>``
 Convert all spaces to underscores.
* ``[p]editor squash <text>``
 Squash all the words into one.
* ``[p]editor title <text>``
 Convert the text to titlecase.
* ``[p]editor trim [trimmer=" "] <text>``
 Trim the outskirts of the text.
* ``[p]editor upper <text>``
 Convert the text to uppercase.
* ``[p]editor wordcount <text>``
 Count the number of words appearing in the text.

------------
Installation
------------

If you haven't added my repo before, lets add it first. We'll call it
"kreusada-cogs" here.

.. code-block:: ini

    [p]repo add kreusada-cogs https://github.com/Kreusada/Kreusada-Cogs

Now, we can install TextEditor.

.. code-block:: ini

    [p]cog install kreusada-cogs texteditor

Once it's installed, it is not loaded by default. Load it by running the following
command:

.. code-block:: ini

    [p]load texteditor

---------------
Further Support
---------------

For more support, head over to the `cog support server <https://discord.gg/GET4DVk>`_,
I have my own channel over there at #support_kreusada-cogs. Feel free to join my
`personal server <https://discord.gg/JmCFyq7>`_ whilst you're here.
