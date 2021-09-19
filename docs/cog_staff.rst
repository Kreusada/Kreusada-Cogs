.. _staff:

=====
Staff
=====

This is the cog guide for the 'Staff' cog. This guide
contains the collection of commands which you can use in the cog.

Through this guide, ``[p]`` will always represent your prefix. Replace
``[p]`` with your own prefix when you use these commands in Discord.

.. note::

    This guide was last updated for version 1.5.5. Ensure
    that you are up to date by running ``[p]cog update staff``.

    If there is something missing, or something that needs improving
    in this documentation, feel free to create an issue `here <https://github.com/Kreusada/Kreusada-Cogs/issues>`_.

    This documentation is auto-generated everytime this cog receives an update.

--------------
About this cog
--------------

This cog will allow you to alert staff using a command, which will be sent
to the specified staff channel. Provides additional details such as the last messages
in the channel, the date, author, and more.

--------
Commands
--------

Here are all the commands included in this cog (5):

* ``[p]staff [reason]``
 Alert for the staff.
* ``[p]staffset``
 Staff notifier configuration.
* ``[p]staffset channel [channel]``
 Sets the channel for staff to receive notifications.
* ``[p]staffset role [role]``
 Sets the Staff role.
* ``[p]staffset settings``
 Show the current settings with Staff.

------------
Installation
------------

If you haven't added my repo before, lets add it first. We'll call it
"kreusada-cogs" here.

.. code-block:: ini

    [p]repo add kreusada-cogs https://github.com/Kreusada/Kreusada-Cogs

Now, we can install Staff.

.. code-block:: ini

    [p]cog install kreusada-cogs staff

Once it's installed, it is not loaded by default. Load it by running the following
command:

.. code-block:: ini

    [p]load staff

---------------
Further Support
---------------

For more support, head over to the `cog support server <https://discord.gg/GET4DVk>`_,
I have my own channel over there at #support_kreusada-cogs. Feel free to join my
`personal server <https://discord.gg/JmCFyq7>`_ whilst you're here.
