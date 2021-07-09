.. _raffle:

======
Raffle
======

This is the cog guide for the raffle cog. You will
find detailed docs about usage and commands.

Throughout this documentation, ``[p]`` is considered as your prefix.

------------
Installation
------------

Let's firstly add my repository if you haven't already:

* :code:`[p]repo add kreusada https://github.com/Kreusada/Kreusada-Cogs`

Next, let's download the cog from the repo:

* :code:`[p]cog install kreusada raffle`

Finally, you can see my end user data statements, cog requirements, and other cog information by using:

* :code:`[p]cog info kreusada raffle`

-----
Usage
-----

This cog allows you to create raffles in your guild, with various conditions
to only allow certain users to join them. Raffles can be edited at any time,
and you can learn more about the condition blocks throughout this documentation.

There are simple and complex raffles. Simple raffles simply include a title and
description, and you can pick multiple users until you decide to end it.

Complex raffles, however, are much more complex (as the name says), as you can
implement various conditions to prevent certain users from joining, or certain
requirements such as account age, roles, and more. They are built using YAML -
which is very easy to get started with. Here's a quick peak into what a complex
raffle would look like, and how it's created:

.. code-block:: yaml

    name: "raffle"
    description: "My very first raffle!"
    end_message: "Congrats {winner.mention} - you've won the {raffle} giveaway!"
    roles_needed_to_enter: [749272596050214973, 798947505193746503]
    prevented_users: [766580519000473640]
    maximum_entries: 5
    account_age: 100 # this is in days

This example does not even include all the conditions, and there will definitely
be more conditions coming in the future.

----------------
Condition Blocks
----------------

^^^^
name
^^^^

The name block is the only required key for a raffle. This block must be under 25
characters in length. It will automatically be converted to lowercase, and will have
all spaces removed from it.

This block must be provided as a str (text with quotes).

Please only use alphanumeric characters, with underscores allowed.

^^^^^^^^^^^
description
^^^^^^^^^^^

The description for your raffle. This information appears in the ``[p]raffle info``
command, so people can see what your raffle's about.

This block must be provided as a str (text with quotes)

^^^^^^^^^^^^
join_message
^^^^^^^^^^^^

A block used to personalize a section of the output when using ``[p]raffle join``.
You can use the special arguments of ``{user}``, ``{entry_count}`` and ``{raffle}``
to customize this message so that it has context.

``raffle``:
    The name of the raffle which the user has joined.

``entry_count``:
    The number of entries in the raffle.

``winner``:
    The member object of the user who joined the raffle.
    The user variable has various attributes, which
    are self explanatory:

    - user.name
    - user.mention
    - user.id
    - user.display_name
    - user.discriminator
    - user.name_and_discriminator

Make sure to use these variables inside curly brackets (``{}``).

If you want to randomize the join_message, simply provide a list of strings.
Otherwise, provide a string by itself.

^^^^^^^^^^^
end_message
^^^^^^^^^^^

A block used to personalize the draw message when using ``[p]raffle draw``. If this key
is not present, the default message is set to "Congratulations {winner.mention}, you have
won the {raffle} raffle!". You can use the special arguments of ``{winner}`` and ``{raffle}``
to customize this message so that it has context.

``raffle``:
    The name of the raffle which the user has won.

``winner``:
    The member object of the user who won the raffle.
    The winner variable has various attributes, which
    are self explanatory:

    - winner.name
    - winner.mention
    - winner.id
    - winner.display_name
    - winner.discriminator
    - winner.name_and_discriminator

Make sure to use these variables inside curly brackets (``{}``).

If you want to randomize the end_message, this is now an option as of version 1.1.0.
Simply provide a list of strings. Otherwise, provide a string by itself.

.. code-block:: yaml

    # randomised
    end_message: ["Congrats {winner.mention}!", "{winner.name} has won the {raffle} raffle."]
    # selected
    end_message: "Congrats {winner.mention}! You have won my {raffle} raffle."

^^^^^^^^^^^
account_age
^^^^^^^^^^^

The required Discord account age for a user to join. This condition is helpful for reducing
"cheaters" who join on alternate accounts in an attempt to have a greater chance at winning.

This condition must be a number, and it must be provided in days. This number cannot be higher
than the Discord app creation date.

^^^^^^^^^^^^^^^
server_join_age
^^^^^^^^^^^^^^^

The required length of time in days that the user must have been in the server for. This condition
is simular to the ``account_age`` condition, but it is instead how long the user has been in the
server for.

This condition must be a number, and it must be provided in days. This number cannot be higher
than the server's creation date.

.. warning::

    The ``join_age`` condition was deprecated for ``server_join_age`` in version 1.2.3.
    Please update to this version, using ``join_age`` is now unsupported and will not work.

^^^^^^^^^^^^^^^^^^^^^
roles_needed_to_enter
^^^^^^^^^^^^^^^^^^^^^

A list of roles which are required in order to join the raffle. This must be a **list** of
role IDs. In case you were unaware, square brackets (``[]``) are used to denote lists.

.. code-block:: yaml

    # Multiple roles
    roles_needed_to_enter: [749272596050214973, 798947505193746503]
    # One role
    roles_needed_to_enter: [749272596050214973]

^^^^^^^^^^^^^^^^^^^^^^
badges_needed_to_enter
^^^^^^^^^^^^^^^^^^^^^^

A list of badges which are required in order to join the raffle. This must be a **list** of
Discord badges. In case you were unaware, square brackets (``[]``) are used to denote lists.

.. code-block:: yaml

    # Multiple badges
    badges_needed_to_enter: ["verified_bot_developer", "bug_hunter"]
    # One badge
    badges_needed_to_enter: ["staff"]

.. tip::

    Available badges: bug_hunter, bug_hunter_level_2, early_supporter, hypesquad,
    hypesquad_balance, hypesquad_bravery, hypesquad_brilliance, partner, staff,
    system, and verified_bot_developer.

^^^^^^^^^^^^^^^
prevented_users
^^^^^^^^^^^^^^^

A list of users who are not allowed to join the raffle. This must be a **list** of
user IDs. Square brackets (``[]``) are used to denote lists.

^^^^^^^^^^^^^
allowed_users
^^^^^^^^^^^^^

A list of users who are allowed to join the raffle. This must be a **list** of
user IDs. Square brackets (``[]``) are used to denote lists.

^^^^^^^^^^^^^^^
maximum_entries
^^^^^^^^^^^^^^^

The maximum number of entries allowed into the raffle. This condition must be
provided as a number.

^^^^^^^^^^^^^
on_end_action
^^^^^^^^^^^^^

This is the prompt for the bot when the a winner is picked for the raffle through
``[p]raffle draw``. Must be one of the following:

* ``end``: The raffle ends immediately after the first winner is picked.
* ``remove_winner``: The winner is removed from the raffle's entries, but the raffle continues.
* ``remove_and_prevent_winner``: The winner is removed from the raffle's entries, and is added to the prevented list.
* ``keep_winner``: The winner stays in the raffle, and could win again.

If not specified, it defaults to ``keep_winner``.

^^^^^^^^^^^^^^
suspense_timer
^^^^^^^^^^^^^^

This condition allows you to set the time for which the bot types when drawing a winner from the raffle.
This must be provided as a number, and must be between 0 and 10.

.. _raffle-commands:

--------
Commands
--------

Here is a list of all commands available for this cog.
There are 31 in total.

.. _raffle-command-raffle:


^^^^^^
raffle
^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle

**Description**

Manage raffles for your server.

.. _raffle-command-raffle-asyaml:

^^^^^^^^^^^^^
raffle asyaml
^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle asyaml <raffle>

**Description**

Get a raffle in its YAML format.

**Arguments:**
    - `<raffle>` - The name of the raffle to get the YAML for.

.. _raffle-command-raffle-conditions:

^^^^^^^^^^^^^^^^^
raffle conditions
^^^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle conditions

**Description**

Get information about how conditions work.

.. _raffle-command-raffle-create:

^^^^^^^^^^^^^
raffle create
^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle create

**Description**

Create a raffle.

.. _raffle-command-raffle-create-complex:

^^^^^^^^^^^^^^^^^^^^^
raffle create complex
^^^^^^^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle create complex

**Description**

Create a raffle with complex conditions.

.. _raffle-command-raffle-create-simple:

^^^^^^^^^^^^^^^^^^^^
raffle create simple
^^^^^^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle create simple <raffle_name> [description]

**Description**

Create a simple arguments with just a name and description.

**Arguments:**
    - `<name>` - The name for the raffle.
    - `[description]` - The description for the raffle.

.. _raffle-command-raffle-docs:

^^^^^^^^^^^
raffle docs
^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle docs

**Description**

Get a link to the docs.

.. _raffle-command-raffle-draw:

^^^^^^^^^^^
raffle draw
^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle draw <raffle>

**Description**

Draw a raffle and select a winner.

**Arguments:**
    - `<raffle>` - The name of the raffle to draw a winner from.

.. _raffle-command-raffle-edit:

^^^^^^^^^^^
raffle edit
^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle edit

**Description**

Edit the settings for a raffle.

.. _raffle-command-raffle-edit-accage:

^^^^^^^^^^^^^^^^^^
raffle edit accage
^^^^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle edit accage <raffle> <new_account_age>

**Description**

Edit the account age requirement for a raffle.

Use `0` or `false` to disable this condition.

**Arguments:**
    - `<raffle>` - The name of the raffle.
    - `<new_account_age>` - The new account age requirement.

.. _raffle-command-raffle-edit-allowed:

^^^^^^^^^^^^^^^^^^^
raffle edit allowed
^^^^^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle edit allowed

**Description**

Manage the allowed users list in a raffle.

.. _raffle-command-raffle-edit-allowed-add:

^^^^^^^^^^^^^^^^^^^^^^^
raffle edit allowed add
^^^^^^^^^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle edit allowed add <raffle> <member>

**Description**

Add a member to the allowed list of a raffle.

**Arguments:**
    - `<raffle>` - The name of the raffle.
    - `<member>` - The member to add to the allowed list.

.. _raffle-command-raffle-edit-allowed-clear:

^^^^^^^^^^^^^^^^^^^^^^^^^
raffle edit allowed clear
^^^^^^^^^^^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle edit allowed clear <raffle>

**Description**

Clear the allowed list for a raffle.

.. _raffle-command-raffle-edit-allowed-remove:

^^^^^^^^^^^^^^^^^^^^^^^^^^
raffle edit allowed remove
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle edit allowed remove <raffle> <member>

**Description**

Remove a member from the allowed list of a raffle.

**Arguments:**
    - `<raffle>` - The name of the raffle.
    - `<member>` - The member to remove from the allowed list.

.. _raffle-command-raffle-edit-convertsimple:

^^^^^^^^^^^^^^^^^^^^^^^^^
raffle edit convertsimple
^^^^^^^^^^^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle edit convertsimple <raffle>

**Description**

Convert a raffle to a simple one (name and description).

**Arguments**
    - ``<raffle>`` - The name of the raffle.

.. _raffle-command-raffle-edit-description:

^^^^^^^^^^^^^^^^^^^^^^^
raffle edit description
^^^^^^^^^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle edit description <raffle> <description>

**Description**

Edit the description for a raffle.

Use `0` or `false` to remove this feature.

**Arguments:**
    - `<raffle>` - The name of the raffle.
    - `<description>` - The new description.

.. _raffle-command-raffle-edit-endmessage:

^^^^^^^^^^^^^^^^^^^^^^
raffle edit endmessage
^^^^^^^^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle edit endmessage <raffle> <end_message>

**Description**

Edit the end message of a raffle.

Once you provide an end message, you will have the chance
to add additional messages, which will be selected at random
when a winner is drawn.

Use ``0`` or ``false`` to disable this condition.

**Arguments:**
    - ``<raffle>`` - The name of the raffle.
    - ``<end_message>`` - The new ending message.

.. _raffle-command-raffle-edit-endaction:

^^^^^^^^^^^^^^^^^^^^^
raffle edit endaction
^^^^^^^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle edit endaction <raffle> <on_end_action>

**Description**

Edit the on_end_action for a raffle.

Use ``0`` or ``false`` to remove this feature.

**Arguments:**
    - ``<raffle>`` - The name of the raffle.
    - ``<on_end_action>`` - The new action. Must be one of ``end``, ``remove_winner``, ``remove_and_prevent_winner``, or ``keep_winner``.

**Arguments:**
    - ``<raffle>`` - The name of the raffle.
    - ``<on_end_action>`` - The new end action.

.. _raffle-command-raffle-edit-fromyaml:

^^^^^^^^^^^^^^^^^^^^
raffle edit fromyaml
^^^^^^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle edit fromyaml <raffle>

Edit a raffle directly from yaml.

**Arguments:**
    - `<raffle>` - The name of the raffle to edit.

.. _raffle-command-raffle-edit-joinage:

^^^^^^^^^^^^^^^^^^^
raffle edit joinage
^^^^^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle edit joinage <raffle> <new_join_age>

**Description**

Edit the join age requirement for a raffle.

Use `0` or `false` to disable this condition.

**Arguments:**
    - `<raffle>` - The name of the raffle.
    - `<new_join_age>` - The new join age requirement.

.. _raffle-command-raffle-edit-joinmessage:

^^^^^^^^^^^^^^^^^^^^^^^
raffle edit joinmessage
^^^^^^^^^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle edit joinmessage <raffle> <joinmessage>

**Description**

Edit the join message of a raffle.

Once you provide a join message, you will have the chance
to add additional messages, which will be selected at random
when a user enters the raffle.

Use ``0`` or ``false`` to disable this condition.

**Arguments:**
    - ``<raffle>`` - The name of the raffle.
    - ``<join_message>`` - The new joining message.

.. _raffle-command-raffle-edit-maxentries:

^^^^^^^^^^^^^^^^^^^^^^
raffle edit maxentries
^^^^^^^^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle edit maxentries <raffle> <maximum_entries>

**Description**

Edit the max entries requirement for a raffle.

Use `0` or `false` to disable this condition.

**Arguments:**
    - `<raffle>` - The name of the raffle.
    - `<maximum_entries>` - The new maximum number of entries.

.. _raffle-command-raffle-edit-prevented:

^^^^^^^^^^^^^^^^^^
raffle edit badges
^^^^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle edit badges

**Description**

Manage badge requirements in a raffle.

.. _raffle-command-raffle-edit-badges-add:

^^^^^^^^^^^^^^^^^^^^^^
raffle edit badges add
^^^^^^^^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle edit badges add <raffle> <badges...>

**Description**

Add badge(s) to the badges requirement list.

**Arguments:**
    - `<raffle>` - The name of the raffle.
    - `<badges...>` - The badge(s) to add to the badge requirement list.

.. _raffle-command-raffle-edit-badges-clear:

^^^^^^^^^^^^^^^^^^^^^^^^
raffle edit badges clear
^^^^^^^^^^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle edit badges clear <raffle>

**Description**

Clear the badge requirements list for a raffle.

**Arguments:**
    - `<raffle>` - The name of the raffle.

.. _raffle-command-raffle-edit-badges-add:

^^^^^^^^^^^^^^^^^^^^^^^^^
raffle edit badges remove
^^^^^^^^^^^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle edit badges remove <raffle> <badges...>

**Description**

Remove badge(s) from the badges requirement list.

**Arguments:**
    - `<raffle>` - The name of the raffle.
    - `<badges...>` - The badge(s) to remove from the badge requirement list.

.. _raffle-command-raffle-edit-prevented:

^^^^^^^^^^^^^^^^^^^^^
raffle edit prevented
^^^^^^^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle edit prevented

**Description**

Manage prevented users in a raffle.

.. _raffle-command-raffle-edit-prevented-add:

^^^^^^^^^^^^^^^^^^^^^^^^^
raffle edit prevented add
^^^^^^^^^^^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle edit prevented add <raffle> <member>

**Description**

Add a member to the prevented list of a raffle.

**Arguments:**
    - `<raffle>` - The name of the raffle.
    - `<member>` - The member to add to the prevented list.

.. _raffle-command-raffle-edit-prevented-clear:

^^^^^^^^^^^^^^^^^^^^^^^^^^^
raffle edit prevented clear
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle edit prevented clear <raffle>

**Description**

Clear the prevented list for a raffle.

**Arguments:**
    - `<raffle>` - The name of the raffle.

.. _raffle-command-raffle-edit-prevented-remove:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^
raffle edit prevented remove
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle edit prevented remove <raffle> <member>

**Description**

Remove a member from the prevented list of a raffle.

**Arguments:**
    - `<raffle>` - The name of the raffle.
    - `<member>` - The member to remove from the prevented list.

.. _raffle-command-raffle-edit-rolesreq:

^^^^^^^^^^^^^^^^^^^^
raffle edit rolesreq
^^^^^^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle edit rolesreq

**Description**

Manage role requirements in a raffle.

.. _raffle-command-raffle-edit-rolesreq-add:

^^^^^^^^^^^^^^^^^^^^^^^^
raffle edit rolesreq add
^^^^^^^^^^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle edit rolesreq add <raffle> <role>

**Description**

Add a role to the role requirements list of a raffle.

**Arguments:**
    - `<raffle>` - The name of the raffle.
    - `<role>` - The role to add to the list of role requirements.

.. _raffle-command-raffle-edit-rolesreq-clear:

^^^^^^^^^^^^^^^^^^^^^^^^^^
raffle edit rolesreq clear
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle edit rolesreq clear <raffle>

**Description**

Clear the role requirements list for a raffle.


**Arguments:**
    - `<raffle>` - The name of the raffle.

.. _raffle-command-raffle-edit-rolesreq-remove:

^^^^^^^^^^^^^^^^^^^^^^^^^^^
raffle edit rolesreq remove
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle edit rolesreq remove <raffle> <role>

**Description**

Remove a role from the role requirements list of a raffle.

**Arguments:**
    - `<raffle>` - The name of the raffle.
    - `<role>` - The role to remove from the list of role requirements.

.. _raffle-command-raffle-edit-stimer:

^^^^^^^^^^^^^^^^^^
raffle edit stimer
^^^^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle edit stimer <raffle> <suspense_timer>

**Description**

Edit the suspense timer for a raffle.

**Arguments:**
    - `<raffle>` - The name of the raffle.
    - `<suspense_timer>` - The new suspense timer for the raffle.

.. _raffle-command-raffle-end:

^^^^^^^^^^
raffle end
^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle end <raffle>

**Description**

End a raffle.

**Arguments:**
    - `<raffle>` - The name of the raffle to end.

.. _raffle-command-raffle-info:

^^^^^^^^^^^
raffle info
^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle info <raffle>

**Description**

Get information about a certain raffle.

**Arguments:**
    - `<raffle>` - The name of the raffle to get information for.

.. _raffle-command-raffle-join:

^^^^^^^^^^^
raffle join
^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle join <raffle>

**Description**

Join a raffle.

**Arguments:**
    - `<raffle>` - The name of the raffle to join.

.. _raffle-command-raffle-kick:

^^^^^^^^^^^
raffle kick
^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle kick <raffle> <member>

**Description**

Kick a member from your raffle.

**Arguments:**
    - `<raffle>` - The name of the raffle.
    - `<member>` - The member to kick from the raffle.

.. _raffle-command-raffle-leave:

^^^^^^^^^^^^
raffle leave
^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle leave <raffle>

**Description**

Leave a raffle.

**Arguments:**
    - `<raffle>` - The name of the raffle to leave.

.. _raffle-command-raffle-list:

^^^^^^^^^^^
raffle list
^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle list

**Description**

List the currently ongoing raffles.

.. _raffle-command-raffle-members:

^^^^^^^^^^^^^^
raffle members
^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle members <raffle>

**Description**

Get all the members of a raffle.

**Arguments:**
    - `<raffle>` - The name of the raffle to get the members from.

.. _raffle-command-raffle-mention:

^^^^^^^^^^^^^^
raffle mention
^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle mention <raffle>

**Description**

Mention all the users entered into a raffle.

**Arguments:**
    - `<raffle>` - The name of the raffle to mention all the members in.

.. _raffle-command-raffle-parse:

^^^^^^^^^^^^
raffle parse
^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle parse

**Description**

Parse a complex raffle without actually creating it.

.. _raffle-command-raffle-raw:

^^^^^^^^^^
raffle raw
^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle raw <raffle>

**Description**

View the raw dictionary for a raffle.

**Arguments:**
    - `<raffle>` - The name of the raffle.

.. _raffle-command-raffle-refresh:

^^^^^^^^^^^^^^
raffle refresh
^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle refresh

**Description**

Refresh all of the raffle caches.

.. _raffle-command-raffle-teardown:

^^^^^^^^^^^^^^^
raffle teardown
^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle teardown

**Description**

End ALL ongoing raffles.

.. _raffle-command-raffle-template:

^^^^^^^^^^^^^^^
raffle template
^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle template

**Description**

Get a template of an example raffle.

.. _raffle-command-raffle-version:

^^^^^^^^^^^^^^
raffle version
^^^^^^^^^^^^^^

**Syntax**

.. code-block:: python

    [p]raffle version

**Description**

Get the version of your Raffle cog.

---------------
Receive Support
---------------

Feel free to ping me at the `Red Cog Support Server <https://discord.gg/GET4DVk>`_ in :code:`#support_kreusada-cogs`.
