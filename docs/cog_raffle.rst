.. _raffle:

======
Raffle
======

This is the cog guide for the 'Raffle' cog. This guide
contains the collection of commands which you can use in the cog.

Through this guide, ``[p]`` will always represent your prefix. Replace
``[p]`` with your own prefix when you use these commands in Discord.

.. note::

    This guide was last updated for version 1.7.3. Ensure
    that you are up to date by running ``[p]cog update raffle``.

    If there is something missing, or something that needs improving
    in this documentation, feel free to create an issue `here <https://github.com/Kreusada/Kreusada-Cogs/issues>`_.

    This documentation is auto-generated everytime this cog receives an update.

--------------
About this cog
--------------

Create raffles for your server.

--------
Commands
--------

Here are all the commands included in this cog (50):

* ``[p]raffle``
 Manage raffles for your server.
* ``[p]raffle asyaml <raffle>``
 Get a raffle in its YAML format.
* ``[p]raffle conditions``
 Get information about how conditions work.
* ``[p]raffle create``
 Create a raffle.
* ``[p]raffle create complex``
 Create a raffle with complex conditions.
* ``[p]raffle create simple <raffle_name> [description]``
 Create a simple arguments with just a name and description.
* ``[p]raffle docs``
 Get a link to the docs.
* ``[p]raffle draw <raffle>``
 Draw a raffle and select a winner.
* ``[p]raffle edit``
 Edit the settings for a raffle.
* ``[p]raffle edit accage <raffle> <new_account_age>``
 Edit the account age requirement for a raffle.
* ``[p]raffle edit allowed``
 Manage the allowed users list in a raffle.
* ``[p]raffle edit allowed add <raffle> <member>``
 Add a member to the allowed list of a raffle.
* ``[p]raffle edit allowed clear <raffle>``
 Clear the allowed list for a raffle.
* ``[p]raffle edit allowed remove <raffle> <member>``
 Remove a member from the allowed list of a raffle.
* ``[p]raffle edit badges``
 Manage required badges in a raffle.
* ``[p]raffle edit badges add <raffle> [badges...]``
 Add a badge to the required badges list of a raffle.
* ``[p]raffle edit badges clear <raffle>``
 Clear the required badges list for a raffle.
* ``[p]raffle edit badges remove <raffle> [badges...]``
 Remove a badge from the required badges list of a raffle.
* ``[p]raffle edit convertsimple <raffle>``
 Convert a raffle to a simple one (name and description).
* ``[p]raffle edit description <raffle> <description>``
 Edit the description for a raffle.
* ``[p]raffle edit endaction <raffle> <on_end_action>``
 Edit the on_end_action for a raffle.
* ``[p]raffle edit endmessage <raffle> <end_message>``
 Edit the end message of a raffle.
* ``[p]raffle edit fromyaml <raffle>``
 Edit a raffle directly from yaml.
* ``[p]raffle edit joinmessage <raffle> <join_message>``
 Edit the join message of a raffle.
* ``[p]raffle edit maxentries <raffle> <maximum_entries>``
 Edit the max entries requirement for a raffle.
* ``[p]raffle edit prevented``
 Manage prevented users in a raffle.
* ``[p]raffle edit prevented add <raffle> <member>``
 Add a member to the prevented list of a raffle.
* ``[p]raffle edit prevented clear <raffle>``
 Clear the prevented list for a raffle.
* ``[p]raffle edit prevented remove <raffle> <member>``
 Remove a member from the prevented list of a raffle.
* ``[p]raffle edit rolesreq``
 Manage role requirements in a raffle.
* ``[p]raffle edit rolesreq add <raffle> <role>``
 Add a role to the role requirements list of a raffle.
* ``[p]raffle edit rolesreq clear <raffle>``
 Clear the role requirement list for a raffle.
* ``[p]raffle edit rolesreq remove <raffle> <role>``
 Remove a role from the role requirements list of a raffle.
* ``[p]raffle edit serverjoinage <raffle> <new_server_join_age>``
 Edit the server join age requirement for a raffle.
* ``[p]raffle edit stimer <raffle> <suspense_timer>``
 Edit the suspense timer for a raffle.
* ``[p]raffle end <raffle>``
 End a raffle.
* ``[p]raffle info <raffle>``
 Get information about a certain raffle.
* ``[p]raffle join <raffle>``
 Join a raffle.
* ``[p]raffle kick <raffle> <member>``
 Kick a member from your raffle.
* ``[p]raffle leave <raffle>``
 Leave a raffle.
* ``[p]raffle list``
 List the currently ongoing raffles.
* ``[p]raffle members <raffle>``
 Get all the members of a raffle.
* ``[p]raffle mention <raffle>``
 Mention all the users entered into a raffle.
* ``[p]raffle parse``
 Parse a complex raffle without actually creating it.
* ``[p]raffle raw <raffle>``
 View the raw dictionary for a raffle.
* ``[p]raffle refresh <raffle>``
 Refresh raffle(s).
* ``[p]raffle refresh global``
 Refresh global raffles.
* ``[p]raffle refresh guild``
 Refresh this guild's raffles.
* ``[p]raffle teardown``
 End ALL ongoing raffles.
* ``[p]raffle version``
 Get the version of your Raffle cog.

------------
Installation
------------

If you haven't added my repo before, lets add it first. We'll call it
"kreusada-cogs" here.

.. code-block:: ini

    [p]repo add kreusada-cogs https://github.com/Kreusada/Kreusada-Cogs

Now, we can install Raffle.

.. code-block:: ini

    [p]cog install kreusada-cogs raffle

Once it's installed, it is not loaded by default. Load it by running the following
command:

.. code-block:: ini

    [p]load raffle

---------------
Further Support
---------------

For more support, head over to the `cog support server <https://discord.gg/GET4DVk>`_,
I have my own channel over there at #support_kreusada-cogs. Feel free to join my
`personal server <https://discord.gg/JmCFyq7>`_ whilst you're here.
