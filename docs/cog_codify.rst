.. _codify:

======
Codify
======

This is the cog guide for the codify cog. You will
find detailed docs about usage and commands.

Throughout this documentation, ``[p]`` is considered as your prefix.

------------
Installation
------------

Let's firstly add my repository if you haven't already:

* :code:`[p]repo add kreusada https://github.com/Kreusada/Kreusada-Cogs`

Next, let's download the cog from the repo:

* :code:`[p]cog install kreusada codify`

Finally, you can see my end user data statements, cog requirements, and other cog information by using:

* :code:`[p]cog info kreusada codify`

-----
Usage
-----

Place text inside of codeblocks.

.. _codify-commands:

--------
Commands
--------

Here's a list of all commands available for this cog.

.. _codify-command-codify-frommsg:

^^^^^^^^^^^^^^
codify frommsg
^^^^^^^^^^^^^^

**Syntax**

.. code-block:: ini

    [p]codify <message_id> [language=python]

**Description**

Get a message and wrap it in a codeblock.

**Arguments**

* ``<message_id>``: The message's ID to convert into a codeblock.
* ``[language]``: The language of the codeblock. If none is provided, it defaults to python.

.. _codify-command-codify-fromtext:

^^^^^^^^^^^^^^^
codify fromtext
^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: ini

    [p]codify [language=python] <text>

**Description**

Get a message and wrap it in a codeblock.

**Arguments**

* ``[language]``: The language of the codeblock. If none is provided, it defaults to python.
* ``<text>``: The text to put inside of the codeblock.

---------------
Receive Support
---------------

Feel free to ping me at the `Red Cog Support Server <https://discord.gg/GET4DVk>`_ in :code:`#support_kreusada-cogs`.
