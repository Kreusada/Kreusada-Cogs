.. _blackformatter:

==============
BlackFormatter
==============

This is the cog guide for the 'BlackFormatter' cog. This guide
contains the collection of commands which you can use in the cog.

Through this guide, ``[p]`` will always represent your prefix. Replace
``[p]`` with your own prefix when you use these commands in Discord.

.. note::

    This guide was last updated for version 1.1.0. Ensure
    that you are up to date by running ``[p]cog update blackformatter``.

    If there is something missing, or something that needs improving
    in this documentation, feel free to create an issue `here <https://github.com/Kreusada/Kreusada-Cogs/issues>`_.

    This documentation is auto-generated everytime this cog receives an update.

--------------
About this cog
--------------

Run black on code.

--------
Commands
--------

Here are all the commands included in this cog (1):

+--------------+----------------------------------------------------------------------------------+
| Command      | Help                                                                             |
+==============+==================================================================================+
| ``[p]black`` | Format a python file with black.                                                 |
|              |                                                                                  |
|              | You need to attach a file to this command, and it's extension needs to be `.py`. |
|              | Your `line_length` is black setting. If it is not provided, it defaults to the   |
|              | configured black line length (the default, unchanged, is 88).                    |
+--------------+----------------------------------------------------------------------------------+

------------
Installation
------------

If you haven't added my repo before, lets add it first. We'll call it
"kreusada-cogs" here.

.. code-block::

    [p]repo add kreusada-cogs https://github.com/Kreusada/Kreusada-Cogs

Now, we can install BlackFormatter.

.. code-block::

    [p]cog install kreusada-cogs blackformatter

Once it's installed, it is not loaded by default. Load it by running the following
command:

.. code-block::

    [p]load blackformatter

---------------
Further Support
---------------

For more support, head over to the `cog support server <https://discord.gg/GET4DVk>`_,
I have my own channel over there at #support_kreusada-cogs. Feel free to join my
`personal server <https://discord.gg/JmCFyq7>`_ whilst you're here.
