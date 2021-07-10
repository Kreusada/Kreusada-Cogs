.. _advanceduptime:

===============
Advanced Uptime
===============

This is the cog guide for the advanceduptime cog. You will
find detailed docs about usage and commands.

Throughout this documentation, ``[p]`` is considered as your prefix.

------------
Installation
------------

Let's firstly add my repository if you haven't already:

* :code:`[p]repo add kreusada https://github.com/Kreusada/Kreusada-Cogs`

Next, let's download the cog from the repo:

* :code:`[p]cog install kreusada advanceduptime`

Finally, you can see my end user data statements, cog requirements, and other cog information by using:

* :code:`[p]cog info kreusada advanceduptime`

-----
Usage
-----

This cog is going to show your bot's uptime, with extra information and stats about the bot.

.. _advanceduptime-commands:

--------
Commands
--------

Here's a list of all commands available for this cog.

.. _advanceduptime-command-uptime:

^^^^^^
uptime
^^^^^^

**Syntax**

.. code-block:: ini

    [p]uptime

**Description**

Shows your bot's uptime and additional stats.

You might be wondering, how are you able to use a new uptime command if one already exists in core?
This cog will replace the core uptime command, and then will add the core uptime command back
if the :code:`AdvancedUptime` cog is unloaded/uninstalled.

This command's output will provide information on your bot's uptime, your bot's name,
your bot's owner (you), the current discord guild, the number of guilds the bot is present in,
the number of unique users your bot has, and the number of commands available!

---------------
Receive Support
---------------

Feel free to ping me at the `Red Cog Support Server <https://discord.gg/GET4DVk>`_ in :code:`#support_kreusada-cogs`.
