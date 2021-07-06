.. _serverblock:

===========
ServerBlock
===========

This is the cog guide for the serverblock cog. You will
find detailed docs about usage and commands.

Throughout this documentation, ``[p]`` is considered as your prefix.

------------
Installation
------------

Let's firstly add my repository if you haven't already:

* :code:`[p]repo add kreusada https://github.com/Kreusada/Kreusada-Cogs`

Next, let's download the cog from the repo:

* :code:`[p]cog install kreusada serverblock`

Finally, you can see my end user data statements, cog requirements, and other cog information by using:

* :code:`[p]cog info kreusada serverblock`

-----
Usage
-----

This cog can stop your bot from joining particular guilds.

.. _serverblock-commands:

--------
Commands
--------

Here's a list of all commands available for this cog.

.. _serverblock-command-sbl:

^^^
sbl
^^^

**Syntax**

.. code-block:: ini

    [p]sbl

**Description**

The base command for serverblock.
You will find all commands under this command.

.. _serverblock-command-sbl-add:

"""""""
sbl add
"""""""

**Syntax**

.. code-block:: ini

    [p]sbl add <server_id>

**Description**

Add a server to the server blocklist.

**Arguments**

* ``<server_id>``: The server's ID to add to the blocklist.

.. _serverblock-command-sbl-remove:

""""""""""
sbl remove
""""""""""

**Syntax**

.. code-block:: ini

    [p]sbl remove <server_id>

**Description**

Remove a server from the server blocklist.

**Arguments**

* ``<server_id>``: The server's ID to remove from the blocklist.

.. _serverblock-command-sbl-clear:

"""""""""
sbl clear
"""""""""

**Syntax**

.. code-block:: ini

    [p]sbl clear

**Description**

Clears the server blocklist.

.. _serverblock-command-sbl-list:

""""""""
sbl list
""""""""

**Syntax**

.. code-block:: ini

    [p]sbl list

**Description**

Get a list of servers on the server blocklist.

---------------
Receive Support
---------------

Feel free to ping me at the `Red Cog Support Server <https://discord.gg/GET4DVk>`_ in :code:`#support_kreusada-cogs`.
