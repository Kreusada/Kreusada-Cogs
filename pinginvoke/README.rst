.. _pinginvoke:

==========
PingInvoke
==========

This is the cog guide for the pinginvoke cog. You will
find detailed docs about usage and commands.

Throughout this documentation, ``[p]`` is considered as your prefix.

------------
Installation
------------

Let's firstly add my repository if you haven't already:

* :code:`[p]repo add kreusada https://github.com/Kreusada/Kreusada-Cogs`

Next, let's download the cog from the repo:

* :code:`[p]cog install kreusada pinginvoke`

Finally, you can see my end user data statements, cog requirements, and other cog information by using:

* :code:`[p]cog info kreusada pinginvoke`

-----
Usage
-----

This cog will invoke the ping command by asking if your bot is there.

For instance, if your bot was called WALL-E, whenever I say "walle?",
it will invoke the ping command. This can be set to whatever you want, as long as it ends in a question mark.

.. tip::

    This cog works amazingly with my PingOverride cog! I suggest you install that too (not required, suggested).

.. _pinginvoke-commands:

--------
Commands
--------

Here's a list of all commands available for this cog.

.. _pinginvoke-command-pingi:

^^^^^
pingi
^^^^^

**Syntax**

.. code-block:: ini

    [p]pingi

**Description**

Commands to configure PingInvoke.

.. _pinginvoke-command-pingi-reset:

"""""""""""
pingi reset
"""""""""""

**Syntax**

.. code-block:: ini

    [p]pingi reset

**Description**

Resets and disables PingInvoke. Your bot will no longer respond if you
call for it.

.. _pinginvoke-command-pingi-set:

"""""""""
pingi set
"""""""""

**Syntax**

.. code-block:: ini

    [p]pingi set <botname>

**Description**

Sets the botname to respond to. This is case insensitive.
For example, if you used ``[p]pingi set walle``, and then you said
"walle?", it would invoke the ping command.

.. note:: There is no need to include the question mark in ``<botname>``.

**Arguments**

* ``<botname>``: The name to listen for.

.. _pinginvoke-command-pingi-settings:

""""""""""""""
pingi settings
""""""""""""""

**Syntax**

.. code-block:: ini

    [p]pingi settings

**Description**

Shows the settings for PingInvoke.

---------------
Receive Support
---------------

Feel free to ping me at the `Red Cog Support Server <https://discord.gg/GET4DVk>`_ in :code:`#support_kreusada-cogs`.
