.. _pingoverride:

============
PingOverride
============

This is the cog guide for the pingoverride cog. You will
find detailed docs about usage and commands.

Throughout this documentation, ``[p]`` is considered as your prefix.

------------
Installation
------------

Let's firstly add my repository if you haven't already:

* :code:`[p]repo add kreusada https://github.com/Kreusada/Kreusada-Cogs`

Next, let's download the cog from the repo:

* :code:`[p]cog install kreusada pingoverride`

Finally, you can see my end user data statements, cog requirements, and other cog information by using:

* :code:`[p]cog info kreusada pingoverride`

-----
Usage
-----

This cog will allow you to customize the response from the ``ping`` command.
So instead of "Pong.", it could be "Beep boop.", or whatever you want!

.. note::

    This cog replaces the core's ``ping`` command. If you wish to have the old ping command
    back, you can simply unload this cog.

.. tip::

    This cog works amazingly with my PingInvoke cog! I suggest you install that too (not required, suggested).

.. _pingoverride-commands:

--------
Commands
--------

.. _pingoverride-command-ping:

^^^^
ping
^^^^

**Syntax**

.. code-block:: none

    [p]ping

**Description**

Pong.

.. _pingoverride-command-pingset:

^^^^^^^
pingset
^^^^^^^

**Syntax**

.. code-block:: none

    [p]pingset

**Description**

Set your ping message.

.. _pingoverride-command-pingset-embed:

"""""""""""""
pingset embed
"""""""""""""

**Syntax**

.. code-block:: none

    [p]pingset embed

**Description**

Manage your ping command's embed.

.. _pingoverride-command-pingset-embed-color:

"""""""""""""""""""
pingset embed color
"""""""""""""""""""

**Syntax**

.. code-block:: none

    [p]pingset embed color [color]

.. tip:: Alias: ``pingset embed colour``

**Description**

Set your embed's color. Leave blank for bot color.

.. _pingoverride-command-pingset-embed-description:

"""""""""""""""""""""""""
pingset embed description
"""""""""""""""""""""""""

**Syntax**

.. code-block:: none

    [p]pingset embed description <description>

**Description**

Set your embed's description.

.. _pingoverride-command-pingset-embed-title:

"""""""""""""""""""
pingset embed title
"""""""""""""""""""

**Syntax**

.. code-block:: none

    [p]pingset embed title <title>

**Description**

Set your embed's title.

.. _pingoverride-command-pingset-message:

"""""""""""""""
pingset message
"""""""""""""""

**Syntax**

.. code-block:: none

    [p]pingset message <ping_message>

.. tip:: Alias: ``pingset response``

**Description**

Set the ping message sent when a user runs the ping command.

**Variables:**

- ``{author.name}``
- ``{author.mention}``
- ``{author.id}``
- ``{author.discriminator}``
`` ``{author.name_and_discriminator}``
- ``{latency}``

.. _pingoverride-command-pingset-reply:

"""""""""""""
pingset reply
"""""""""""""

**Syntax**

.. code-block:: none

    [p]pingset reply <reply>

**Description**

Set whether the ping message uses replies.

.. _pingoverride-command-pingset-reply-mention:

"""""""""""""""""""""
pingset reply mention
"""""""""""""""""""""

**Syntax**

.. code-block:: none

    [p]pingset reply mention <mention>

**Description**

Set whether the ping message uses replies.

.. _pingoverride-command-pingset-settings:

""""""""""""""""
pingset settings
""""""""""""""""

**Syntax**

.. code-block:: none

    [p]pingset settings

**Description**

See the current settings for PingOverride.

.. _pingoverride-command-pingset-variables:

"""""""""""""""""
pingset variables
"""""""""""""""""

**Syntax**

.. code-block:: none

    [p]pingset variables

.. tip:: Alias: ``pingset vars``

**Description**

List the available variables for the ping command.

---------------
Receive Support
---------------

Feel free to ping me at the `Red Cog Support Server <https://discord.gg/GET4DVk>`_ in :code:`#support_kreusada-cogs`.
