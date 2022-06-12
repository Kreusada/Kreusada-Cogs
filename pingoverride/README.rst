.. _pingoverride:

============
PingOverride
============

This is the cog guide for the 'PingOverride' cog. This guide
contains the collection of commands which you can use in the cog.

Through this guide, ``[p]`` will always represent your prefix. Replace
``[p]`` with your own prefix when you use these commands in Discord.

.. note::

    This guide was last updated for version 3.6.0. Ensure
    that you are up to date by running ``[p]cog update pingoverride``.

    If there is something missing, or something that needs improving
    in this documentation, feel free to create an issue `here <https://github.com/Kreusada/Kreusada-Cogs/issues>`_.

    This documentation is auto-generated everytime this cog receives an update.

--------------
About this cog
--------------

Override the Core's ping command with your own response.

--------
Commands
--------

Here are all the commands included in this cog (13):

* ``[p]ping``
 Pong.
* ``[p]pingset``
 Set your ping message.
* ``[p]pingset embed``
 Manage the embed settings for the ping command.
* ``[p]pingset embed title [title]``
 Set the title for the embed.
* ``[p]pingset embed toggle <toggle>``
 Toggle whether embeds should be enabled for the ping command.
* ``[p]pingset invoke``
 Commands to configure invoking ping.
* ``[p]pingset invoke reset``
 Reset and disable PingInvoke.
* ``[p]pingset invoke set <botname>``
 Set the bot name to listen for.
* ``[p]pingset invoke settings``
 Show the current settings for PingInvoke.
* ``[p]pingset message <ping_message>``
 Set the ping message sent when a user runs the ping command.
* ``[p]pingset reply <reply>``
 Set whether the ping message uses replies.
* ``[p]pingset reply mention <mention>``
 Set whether the ping message uses replies.
* ``[p]pingset settings``
 See the current settings for PingOverride.

------------
Installation
------------

If you haven't added my repo before, lets add it first. We'll call it
"kreusada-cogs" here.

.. code-block:: ini

    [p]repo add kreusada-cogs https://github.com/Kreusada/Kreusada-Cogs

Now, we can install PingOverride.

.. code-block:: ini

    [p]cog install kreusada-cogs pingoverride

Once it's installed, it is not loaded by default. Load it by running the following
command:

.. code-block:: ini

    [p]load pingoverride

---------------
Further Support
---------------

For more support, head over to the `cog support server <https://discord.gg/GET4DVk>`_,
I have my own channel over there at #support_kreusada-cogs. Feel free to join my
`personal server <https://discord.gg/JmCFyq7>`_ whilst you're here.
