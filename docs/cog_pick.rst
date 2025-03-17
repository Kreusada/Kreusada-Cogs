.. _pick:

====
Pick
====

This is the cog guide for the 'Pick' cog. This guide
contains the collection of commands which you can use in the cog.

Through this guide, ``[p]`` will always represent your prefix. Replace
``[p]`` with your own prefix when you use these commands in Discord.

.. note::

    This guide was last updated for version 1.0.1. Ensure
    that you are up to date by running ``[p]cog update pick``.

    If there is something missing, or something that needs improving
    in this documentation, feel free to create an issue `here <https://github.com/Kreusada/Kreusada-Cogs/issues>`_.

    This documentation is auto-generated everytime this cog receives an update.

--------------
About this cog
--------------

Pick a random member.

--------
Commands
--------

Here are all the commands included in this cog (2):

+---------------+-------------------------------------------------------------------------------------------------+
| Command       | Help                                                                                            |
+===============+=================================================================================================+
| ``[p]pick``   | Pick a random member. You may supply a role to pick from.                                       |
+---------------+-------------------------------------------------------------------------------------------------+
| ``[p]pickid`` | Pick a random member, displaying the ID only. You may supply a role to pick from.               |
|               |                                                                                                 |
|               | This can be integrated with [nestedcommands by tmerc](https://github.com/tmercswims/tmerc-cogs) |
|               | Example of usage: `[p]say Congratulations <@$(pick True)>! You won!`                            |
+---------------+-------------------------------------------------------------------------------------------------+

------------
Installation
------------

If you haven't added my repo before, lets add it first. We'll call it
"kreusada-cogs" here.

.. code-block::

    [p]repo add kreusada-cogs https://github.com/Kreusada/Kreusada-Cogs

Now, we can install Pick.

.. code-block::

    [p]cog install kreusada-cogs pick

Once it's installed, it is not loaded by default. Load it by running the following
command:

.. code-block::

    [p]load pick

---------------
Further Support
---------------

For more support, head over to the `cog support server <https://discord.gg/GET4DVk>`_,
I have my own channel over there at #support_kreusada-cogs. Feel free to join my
`personal server <https://discord.gg/JmCFyq7>`_ whilst you're here.
