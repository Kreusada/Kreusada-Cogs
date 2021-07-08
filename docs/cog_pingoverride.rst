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

Pong. Or not?

.. _pingoverride-command-pingset:

^^^^^^^
pingset
^^^^^^^

.. note:: |owner-lock|

**Syntax**

.. code-block:: none

    [p]pingset 

**Description**

Settings for ping.

.. _pingoverride-command-pingset-embed:

"""""""""""""
pingset embed
"""""""""""""

**Syntax**

.. code-block:: none

    [p]pingset embed <true_or_false>

**Description**

Toggle whether to use embeds in replies.

Your message will be put into the description.
Embeds will not send if they have been disabled via ``[p]embedset``.

.. _pingoverride-command-pingset-message:

"""""""""""""""
pingset message
"""""""""""""""

**Syntax**

.. code-block:: none

    [p]pingset message <message>

**Description**

Set your custom ping message.

Optional Regex:
``{author}``: Replaces with the authors display name.
``{latency}``: Replaces with the bots latency.

Example Usage:
``[p]pingset message Hello {author}! My latency is {latency} ms.``

Random Responses:
When you specify ``<message>``, you will be asked if you want to add
more responses. These responses will be chosen at random when you run the
ping command.

To exit out of the random selection session, type ``stop()`` or ``exit()``.

.. _pingoverride-command-pingset-regex:

"""""""""""""
pingset regex
"""""""""""""

**Syntax**

.. code-block:: none

    [p]pingset regex 

**Description**

Get information on the types of ping regex.

.. _pingoverride-command-pingset-reply:

"""""""""""""
pingset reply
"""""""""""""

**Syntax**

.. code-block:: none

    [p]pingset reply <true_or_false> [mention=False]

**Description**

Set whether ping will use replies in their output.

.. _pingoverride-command-pingset-settings:

""""""""""""""""
pingset settings
""""""""""""""""

**Syntax**

.. code-block:: none

    [p]pingset settings 

**Description**

Get the settings for the ping command.

---------------
Receive Support
---------------

Feel free to ping me at the `Red Cog Support Server <https://discord.gg/GET4DVk>`_ in :code:`#support_kreusada-cogs`.