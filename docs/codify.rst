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

* :code:`[p]repo add kreusada https://github.com/kreusada/kreusadacogs`

Next, let's download the cog from the repo:

* :code:`[p]cog install kreusada codify`

Finally, you can see my end user data statements, cog requirements, and other cog information by using:

* :code:`[p]cog info kreusada codify`

-----
Usage
-----

This cog is going to return spoilers with ``pop`` inside them, so that you can metaphorically pop bubblewrap!

.. _codify-commands:

--------
Commands
--------

Here's a list of all commands available for this cog.

.. _codify-command-codify:

^^^^^^
codify
^^^^^^

**Syntax**

.. code-block:: ini

    [p]codify <message_id> [language=python] [escape_markdown=False]

**Description**

Get a message and wrap it in a codeblock.

**Arguments**

* ``<message_id>``: The message's ID to convert into a codeblock.
* ``[language]``: The language of the codeblock. If none is provided, it defaults to python.
* ``[escape_markdown]``: Determines whether to escape the ``<message_id>``. If none is provided, it defaults to False.

----------------------
Additional Information
----------------------

This cog has been vetted by the Red-DiscordBot QA team as approved.
For inquiries, see to the contact options below.

---------------
Receive Support
---------------

Feel free to ping me at the `Red Cog Support Server <https://discord.gg/GET4DVk>`_ in :code:`#support_othercogs`,
or you can head over to `my support server <https://discord.gg/JmCFyq7>`_ and ask your questions in :code:`#support-kreusadacogs`.