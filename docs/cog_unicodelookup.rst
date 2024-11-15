.. _unicodelookup:

=============
UnicodeLookup
=============

This is the cog guide for the 'UnicodeLookup' cog. This guide
contains the collection of commands which you can use in the cog.

Through this guide, ``[p]`` will always represent your prefix. Replace
``[p]`` with your own prefix when you use these commands in Discord.

.. note::

    This guide was last updated for version 1.0.0. Ensure
    that you are up to date by running ``[p]cog update unicodelookup``.

    If there is something missing, or something that needs improving
    in this documentation, feel free to create an issue `here <https://github.com/Kreusada/Kreusada-Cogs/issues>`_.

    This documentation is auto-generated everytime this cog receives an update.

--------------
About this cog
--------------

Search the unicode library for characters and names. Supports fuzzy searching.

--------
Commands
--------

Here are all the commands included in this cog (4):

* ``[p]ulookup``
    Unicode lookup commands.
* ``[p]ulookup char <name>``
    Get the unicode character from the name.
* ``[p]ulookup fuzzy [strength=80] <term>``
    Get unicode characters from the fuzzy search term.

   Strength must be a number from 50 to 100, used by the fuzzy search algorithm. Defaults to 80 (recommended).
* ``[p]ulookup name <characters>``
    Get the unicode names of characters.

------------
Installation
------------

If you haven't added my repo before, lets add it first. We'll call it
"kreusada-cogs" here.

.. code-block:: ini

    [p]repo add kreusada-cogs https://github.com/Kreusada/Kreusada-Cogs

Now, we can install UnicodeLookup.

.. code-block:: ini

    [p]cog install kreusada-cogs unicodelookup

Once it's installed, it is not loaded by default. Load it by running the following
command:

.. code-block:: ini

    [p]load unicodelookup

---------------
Further Support
---------------

For more support, head over to the `cog support server <https://discord.gg/GET4DVk>`_,
I have my own channel over there at #support_kreusada-cogs. Feel free to join my
`personal server <https://discord.gg/JmCFyq7>`_ whilst you're here.
