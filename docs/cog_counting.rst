.. _counting:

========
Counting
========

This is the cog guide for the 'Counting' cog. This guide
contains the collection of commands which you can use in the cog.

Through this guide, ``[p]`` will always represent your prefix. Replace
``[p]`` with your own prefix when you use these commands in Discord.

.. note::

    This guide was last updated for version 1.5.2. Ensure
    that you are up to date by running ``[p]cog update counting``.

    If there is something missing, or something that needs improving
    in this documentation, feel free to create an issue `here <https://github.com/Kreusada/Kreusada-Cogs/issues>`_.

    This documentation is auto-generated everytime this cog receives an update.

--------------
About this cog
--------------

Make a counting channel with goals.

--------
Commands
--------

Here are all the commands included in this cog (9):

+--------------------------+-------------------------------------------------------------------------------------------------------+
| Command                  | Help                                                                                                  |
+==========================+=======================================================================================================+
| ``[p]countset``          | Various Counting settings.                                                                            |
+--------------------------+-------------------------------------------------------------------------------------------------------+
| ``[p]countset channel``  | Set the counting channel.                                                                             |
|                          |                                                                                                       |
|                          | If channel isn't provided, it will delete the current channel.                                        |
+--------------------------+-------------------------------------------------------------------------------------------------------+
| ``[p]countset goal``     | Set the counting goal.                                                                                |
|                          |                                                                                                       |
|                          | If goal isn't provided, it will be deleted.                                                           |
+--------------------------+-------------------------------------------------------------------------------------------------------+
| ``[p]countset reset``    | Reset the counter and start from 0 again!                                                             |
+--------------------------+-------------------------------------------------------------------------------------------------------+
| ``[p]countset role``     | Add a whitelisted role.                                                                               |
+--------------------------+-------------------------------------------------------------------------------------------------------+
| ``[p]countset settings`` | See current settings.                                                                                 |
+--------------------------+-------------------------------------------------------------------------------------------------------+
| ``[p]countset start``    | Set the starting number.                                                                              |
+--------------------------+-------------------------------------------------------------------------------------------------------+
| ``[p]countset topic``    | Toggle counting channel's topic changing.                                                             |
|                          |                                                                                                       |
|                          | If `on_off` is not provided, the state will be flipped.=                                              |
+--------------------------+-------------------------------------------------------------------------------------------------------+
| ``[p]countset warnmsg``  | Toggle a warning message.                                                                             |
|                          |                                                                                                       |
|                          | If `on_off` is not provided, the state will be flipped.                                               |
|                          | Optionally add how many seconds the bot should wait before deleting the message (0 for not deleting). |
+--------------------------+-------------------------------------------------------------------------------------------------------+

------------
Installation
------------

If you haven't added my repo before, lets add it first. We'll call it
"kreusada-cogs" here.

.. code-block::

    [p]repo add kreusada-cogs https://github.com/Kreusada/Kreusada-Cogs

Now, we can install Counting.

.. code-block::

    [p]cog install kreusada-cogs counting

Once it's installed, it is not loaded by default. Load it by running the following
command:

.. code-block::

    [p]load counting

---------------
Further Support
---------------

For more support, head over to the `cog support server <https://discord.gg/GET4DVk>`_,
I have my own channel over there at #support_kreusada-cogs. Feel free to join my
`personal server <https://discord.gg/JmCFyq7>`_ whilst you're here.
