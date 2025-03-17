.. _lock:

====
Lock
====

This is the cog guide for the 'Lock' cog. This guide
contains the collection of commands which you can use in the cog.

Through this guide, ``[p]`` will always represent your prefix. Replace
``[p]`` with your own prefix when you use these commands in Discord.

.. note::

    This guide was last updated for version 2.0.1. Ensure
    that you are up to date by running ``[p]cog update lock``.

    If there is something missing, or something that needs improving
    in this documentation, feel free to create an issue `here <https://github.com/Kreusada/Kreusada-Cogs/issues>`_.

    This documentation is auto-generated everytime this cog receives an update.

--------------
About this cog
--------------

Lock `@everyone` from sending messages in channels or the entire guild, and only allow Moderators to talk.

--------
Commands
--------

Here are all the commands included in this cog (10):

+-------------------------+--------------------------------------------------------------+
| Command                 | Help                                                         |
+=========================+==============================================================+
| ``[p]lock``             | Lock `@everyone` from sending messages.                      |
+-------------------------+--------------------------------------------------------------+
| ``[p]lock server``      | Lock `@everyone` from sending messages in the entire server. |
+-------------------------+--------------------------------------------------------------+
| ``[p]lockset``          | Various Lock settings.                                       |
+-------------------------+--------------------------------------------------------------+
| ``[p]lockset ignore``   | Ignore a channel during server lock.                         |
+-------------------------+--------------------------------------------------------------+
| ``[p]lockset perms``    | Set if you use roles to access channels.                     |
+-------------------------+--------------------------------------------------------------+
| ``[p]lockset role``     | Set role that can lock channels.                             |
+-------------------------+--------------------------------------------------------------+
| ``[p]lockset settings`` | See current settings.                                        |
+-------------------------+--------------------------------------------------------------+
| ``[p]lockset unignore`` | Remove channels from the ignored list.                       |
+-------------------------+--------------------------------------------------------------+
| ``[p]unlock``           | Unlock the channel for `@everyone`.                          |
+-------------------------+--------------------------------------------------------------+
| ``[p]unlock server``    | Unlock the entire server for `@everyone`                     |
+-------------------------+--------------------------------------------------------------+

------------
Installation
------------

If you haven't added my repo before, lets add it first. We'll call it
"kreusada-cogs" here.

.. code-block:: ini

    [p]repo add kreusada-cogs https://github.com/Kreusada/Kreusada-Cogs

Now, we can install Lock.

.. code-block:: ini

    [p]cog install kreusada-cogs lock

Once it's installed, it is not loaded by default. Load it by running the following
command:

.. code-block:: ini

    [p]load lock

---------------
Further Support
---------------

For more support, head over to the `cog support server <https://discord.gg/GET4DVk>`_,
I have my own channel over there at #support_kreusada-cogs. Feel free to join my
`personal server <https://discord.gg/JmCFyq7>`_ whilst you're here.
