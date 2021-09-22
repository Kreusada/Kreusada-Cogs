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

----------
Conditions
----------

This section of the documentation will give you an insight into some
of the conditions you can include in your raffles.

***********
account_age
***********

This condition can prevent people from joining your raffle if their account age
in days is below the required amount. Provide this condition as a number, as a representation
of the account age requirement in **days**.

**Example usage**

.. code-block:: yaml
    
    account_age: 30

*************
allowed_users
*************

This condition will allow only certain individuals to join the raffle. This is essentially a raffle
whitelist. Provide users as a list, with their IDs.

**Example usage**

.. code-block:: yaml

    allowed_users: [123456780, 987654321, 2468013579]

**********************
badges_needed_to_enter
**********************

This condition only allows users that have specified badges.

**Available badges**

* bug_hunter
* bug_hunter_level_2
* early_supporter
* hypesquad
* hypesquad_balance
* hypesquad_bravery
* hypesquad_brilliance
* partner
* staff
* system
* verified_bot_developer

**Example usage**

.. code-block:: yaml

    badges_needed_to_enter: ["hypesquad_bravery", "verified_bot_developer"]

***********
description
***********

This is the description for your raffle. It's completely optional, and will appear in various
commands such as ``[p]raffle info`` and ``[p]raffle list``. It's objective is to give your users
the best understanding of what your raffle is about.

**Example usage**

.. code-block:: yaml

    description: "This raffle contains not 1, but multiple prizes!"

***********
end_message
***********

This message is sent at the end of the raffle, when the winner is drawn from the pool.
There are various variables you can use to customize the output further.

**Variables**

* {raffle}
* {winner.name}
* {winner.mention}
* {winner.id}
* {winner.display_name}
* {winner.discriminator}
* {winner.name_and_discriminator}

**Example usage**

.. code-block:: yaml

    end_message: "Congratulations {winner.mention}! You have won the {raffle} raffle. :tada:"

************
join_message
************

This message is sent when a user joins the raffle.
There are various variables you can use to customize the output further.

**Variables**

* {raffle}
* {entry_count}
* {user.name}
* {user.mention}
* {user.id}
* {user.display_name}
* {user.discriminator}
* {user.name_and_discriminator}

**Example usage**

.. code-block:: yaml

    end_message: "Welcome to the {raffle} raffle {user.mention}! There are now {entry_count} entries."

***************
maximum_entries
***************

This conditions allows you to limit the number of entries that this raffle can take.
Once the limit is reached, no more users will be able to join, unless a previous user
was kicked, or they left themselves.

**Example usage**

.. code-block:: yaml

    maximum_entries: 10

****
name
****

This key is **required**. This is used as the name of the raffle.

* Must be provided as a string (a word encased with quotation marks).
* Must be under 25 characters in length.
* Must be made up of alphanumeric characters (may also contain an underscore).
* The use of spaces is forbidden. Use underscores instead.

**Example usage**

.. code-block:: yaml

    name: "kreusada_raffle"

*************
on_end_action
*************

This is the prompt for the bot when the a winner is picked for the raffle through
``[p]raffle draw``. Must be one of the following:

* ``end``: The raffle ends immediately after the first winner is picked.
* ``remove_winner``: The winner is removed from the raffle's entries, but the raffle continues.
* ``remove_and_prevent_winner``: The winner is removed from the raffle's entries, and is added to the prevented list.
* ``keep_winner``: The winner stays in the raffle, and could win again.

If not specified, it defaults to ``keep_winner``.

**Example usage**

.. code-block:: yaml

    on_end_action: remove_and_prevent_winner

***************
prevented_users
***************

This condition will block certain individuals from joining the raffle. This is essentially a raffle
blacklist. Provide users as a list, with their IDs.

**Example usage**

.. code-block:: yaml

    prevented_users: [123456780, 987654321, 2468013579]

***************
server_join_age
***************

The required length of time in days that the user must have been in the server for. This condition
is simular to the ``account_age`` condition, but it is instead how long the user has been in the
server for.

This condition must be a number, and it must be provided in days. This number cannot be higher
than the server's creation date.

.. warning::

    The ``join_age`` condition was deprecated for ``server_join_age`` in version 1.2.3.
    Please update to this version, using ``join_age`` is now unsupported and will not work.

**Example usage**

.. code-block:: yaml

    server_join_age: 15

**************
suspense_timer
**************

This condition allows you to set the time for which the bot types when drawing a winner from the raffle.
This must be provided as a number, and must be between 0 and 10.

**Example usage**

.. code-block:: yaml

    suspense_timer: 3

*********************
roles_needed_to_enter
*********************

A list of roles which are required in order to join the raffle. This must be a list of
role IDs.

**Example usage**

.. code-block:: yaml

    # Multiple roles
    roles_needed_to_enter: [123456789, 987654321]
    # One role
    roles_needed_to_enter: [123456789]

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
