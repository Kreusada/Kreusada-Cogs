.. _staff:

=====
Staff
=====

This is the cog guide for the staff cog. You will
find detailed docs about usage and commands.

Throughout this documentation, ``[p]`` is considered as your prefix.

------------
Installation
------------

Let's firstly add my repository if you haven't already:

* :code:`[p]repo add kreusada https://github.com/Kreusada/Kreusada-Cogs`

Next, let's download the cog from the repo:

* :code:`[p]cog install kreusada staff`

Finally, you can see my end user data statements, cog requirements, and other cog information by using:

* :code:`[p]cog info kreusada staff`

-----
Usage
-----

This cog will allow you to alert staff using a command, which will be sent
to the specified staff channel. Provides additional details such as the last messages
in the channel, the date, author, and more.

.. _staff-commands:

--------
Commands
--------

Here's a list of all commands available for this cog.

.. _staff-command-staff:

^^^^^
staff
^^^^^

**Syntax**

.. code-block:: ini

    [p]staff

**Description**

Alert the staff members.

.. _staff-command-staffset:

^^^^^^^^
staffset
^^^^^^^^

**Syntax**

.. code-block:: ini

    [p]staffset

**Description**

Commands to configure the staff cog.

.. _staff-command-staffset-channel:

""""""""""""""""
staffset channel
""""""""""""""""

**Syntax**

.. code-block:: ini

    [p]staffset channel [channel]

**Description**

Set the channel to receive alerts for staff.

**Arguments**

* ``[channel]``: The channel used for notifications. If none provided, it resets.

.. _staff-command-staffset-role:

"""""""""""""
staffset role
"""""""""""""

**Syntax**

.. code-block:: ini

    [p]staffset role [role]

**Description**

Set the staff role to be pinged for staff alerts.

**Arguments**

* ``[role]``: The staff role. This is optional. If none provided, it resets.

---------------
Receive Support
---------------

Feel free to ping me at the `Red Cog Support Server <https://discord.gg/GET4DVk>`_ in :code:`#support_kreusada-cogs`.
