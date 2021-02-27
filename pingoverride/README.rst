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

* :code:`[p]repo add kreusada https://github.com/kreusada/kreusadacogs`

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

.. _pingoverride-commands:

--------
Commands
--------

Here's a list of all commands available for this cog.

.. _pingoverride-command-ping:

^^^^
ping
^^^^

**Syntax**

.. code-block:: ini

    [p]ping

**Description**

Pong? Or not?

Replies with all the PingOverride settings, and your configured response.

.. _pinginvoke-command-pingset:

^^^^^^^
pingset
^^^^^^^

**Syntax**

.. code-block:: ini

    [p]pingset

**Description**

Commands to configure PingOverride. Settings include:

* Embed send
* Replies
* Reply mentions
* Response with special regex

.. _pinginvoke-command-pingset-embed:

^^^^^^^^^^^^^
pingset embed
^^^^^^^^^^^^^

**Syntax**

.. code-block:: ini

    [p]pingset embed <true_or_false>

**Description**

Sets whether the response is sent inside an embed.
On cog install, this setting is false.

.. note:: If the bot doesn't have permissions to send embeds, this setting will be bypassed.

**Arguments**

* ``<true_or_false>``: Toggle for embeds setting. Must specify ``true`` or ``false``.

.. _pinginvoke-command-pingset-message:

^^^^^^^^^^^^^^^
pingset message
^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: ini

    [p]pingset message <response>

**Description**

Set the message that is sent via the ``ping`` command.

Example Usage: ``[p]pingset message Hello {display}! My latency is {latency} ms.``

**Response Regex**

* ``{display}`` - Replaced with the author's display name.
* ``{latency}`` - Replaces with the bot's latency.

**Arguments**

* ``<response>``: The message that is sent via the ``ping`` command.

.. _pinginvoke-command-pingset-reply:

^^^^^^^^^^^^^
pingset reply
^^^^^^^^^^^^^

**Syntax**

.. code-block:: ini

    [p]pingset reply <true_or_false> [mention=False]

**Description**

Toggles whether the ping response will use Discord replies. 
Additionally, you can toggle this to mention, or not.

**Arguments**

* ``<true_or_false>``: Toggle for the replies setting. Must specify ``true`` or ``false``.
* ``[mention=False]``: Toggle whether replies will mention. Specify ``true`` or ``false``. Defaults to False.

.. _pinginvoke-command-pingset-settings:

^^^^^^^^^^^^^^^^
pingset settings
^^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: ini

    [p]pingset settings

**Description**

Shows the settings for PingOverride.

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