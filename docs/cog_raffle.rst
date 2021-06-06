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

The name block is the only required key for a raffle. This block must be under 15
characters in length. It will automatically be converted to lowercase, and will have
all spaces removed from it.

This block must be provided as a str (text with quotes)

**Potential Exceptions**

.. code-block:: yaml
    
    RequiredKeyError: The "name" key is required

This exception is raised when the name key is missing, because it is required. To fix
this, simply add the name key inside of your YAML.

.. code-block:: yaml
    
    BadArgument: Name must be str, not [invalid type]

This exception is raised when the name was not provided in the correct type. A simple fix for
this would be to place quotation marks around your name content.

.. code-block:: yaml

    BadArgument: Name must be under 15 characters, your raffle name had [count]

This exception is raised when your name content has over 15 characters. Be sure to keep it
nice and short, and then try again with a new name which is under 15 characters.

.. code-block:: yaml

    BadArgument: Name must only contain alphanumeric characters, found %.
    Invalid character: hello_there%
                                  ^

This exception is raised when your name contains a non-alphanumeric character. Please only
use letters or numbers in your raffle name. 

.. note::

    Underscores are excluded from this alphanumeric rule, so feel free to use them too.

^^^^^^^^^^^
description
^^^^^^^^^^^

The description for your raffle. This information appears in the ``[p]raffle info`` 
command, so people can see what your raffle's about.

This block must be provided as a str (text with quotes)

**Potential Exceptions**

.. code-block:: yaml
    
    BadArgument: Description must be str, not [invalid type]

This exception is raised when the description was not provided in the correct type. A simple fix for
this would be to place quotation marks around your description's content.

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
        - winner.name_and_descriminator
    
Make sure to use these variables inside curly brackets (``{}``).
This condition must be provided as a str (text with quotes).

**Potential Exceptions**

.. code-block:: yaml
    
    BadArgument: End message must be str

This exception is raised when the end_message was not provided in the correct type. A simple fix 
for this would be to place quotation marks around your end message's content.

.. code-block:: yaml 

    BadArgument: [arg] was an unexpected argument in your end_message block

This exception is raised when the end_message contains an incorrect argument. For example,
``{winner.abc}``, or ``{something_that_doesn't_exist}``. These variables do not exist, nor 
does the ``winner`` variable have an attribute "abc", therefore this exception is raised. 
Please see above for the list of accepted variables.

^^^^^^^^^^^
account_age
^^^^^^^^^^^

The required Discord account age for a user to join. This condition is helpful for reducing 
"cheaters" who join on alternate accounts in an attempt to have a greater chance at winning.

This condition must be a number, and it must be provided in days. This number cannot be higher
than the Discord app creation date.

**Potential Exceptions**

.. code-block:: yaml
    
    BadArgument: Account age days must be int, not [invalid type]

This exception is raised when the account_age was not provided in the correct type. 
Please simply provide a number for this condition, without quotes.

.. code-block:: yaml 

    BadArgument: Account age days must be less than Discord's creation date

This exception is raised when the account_age number is higher than the number of days that 
Discord has existed for. Please try and choose a lower number to make it more realistic.

^^^^^^^^
join_age
^^^^^^^^

The required length of time in days that the user must have been in the server for. This condition
is simular to the ``account_age`` condition, but it is instead how long the user has been in the
server for. 

This condition must be a number, and it must be provided in days. This number cannot be higher
than the server's creation date.

**Potential Exceptions**

.. code-block:: yaml
    
    BadArgument: Join age days must be int, not [invalid type]

This exception is raised when the join_age was not provided in the correct type. 
Please simply provide a number for this condition, without quotes.

.. code-block:: yaml 

    BadArgument: Join age days must be less than this guild's creation date

This exception is raised when the join_age number is higher than the number of days that 
the current server has existed for. Please try and choose a lower number to make it compatible.

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

**Potential Exceptions**

.. code-block:: yaml
    
    BadArgument: Roles must be a list of Discord role IDs, not [invalid type]

This exception is raised when the roles_needed_to_enter was not provided in the correct format. 
Please provide your discord roles via IDs, and in the format shown above in the example.

.. code-block:: yaml 

    BadArgument: <role id> was not a valid role

This exception is raised when one of the roles provided was not found in the current guild.

^^^^^^^^^^^^^^^
prevented_users
^^^^^^^^^^^^^^^

A list of users who are not allowed to join the raffle. This must be a **list** of 
user IDs. Square brackets (``[]``) are used to denote lists.

**Potential Exceptions**

.. code-block:: yaml
    
    BadArgument: Users must be a list of Discord user IDs, not [invalid type]

This exception is raised when the prevented_users was not provided in the correct format. 
Please provide your discord users via IDs, in a list.

.. code-block:: yaml 

    UnknownEntityError: <user id> was not a valid user

This exception is raised when one of the users provided was not found in the current guild.

^^^^^^^^^^^^^
allowed_users
^^^^^^^^^^^^^

A list of users who are allowed to join the raffle. This must be a **list** of 
user IDs. Square brackets (``[]``) are used to denote lists.

**Potential Exceptions**

.. code-block:: yaml
    
    BadArgument: Users must be a list of Discord user IDs, not [invalid type]

This exception is raised when the allowed_users was not provided in the correct format. 
Please provide your discord users via IDs, in a list.

.. code-block:: yaml 

    UnknownEntityError: <user id> was not a valid user

This exception is raised when one of the users provided was not found in the current guild.

^^^^^^^^^^^^^^^
maximum_entries
^^^^^^^^^^^^^^^

The maximum number of entries allowed into the raffle. This condition must be 
provided as a number.

**Potential Exceptions**

.. code-block:: yaml
    
    BadArgument: Maximum entries must be int, not [invalid type]

This exception is raised when the maximum_entries was not provided in the correct type. 
Please simply provide a number for this condition, without quotes.

^^^^^^^^^^^^^
on_end_action
^^^^^^^^^^^^^

This is the prompt for the bot when the a winner is picked for the raffle through
``[p]raffle draw``. Must be one of the following:

* ``end``: The raffle ends immediately after the first winner is picked.
* ``remove_winner``: The winner is removed from the raffle's entries, but the raffle continues.
* ``keep_winner``: The winner stays in the raffle, and could win again.

If not specified, it defaults to ``keep_winner``.

**Potential Exceptions**

.. code-block:: yaml
    
    BadArgument: on_draw_action must be one of 'end', 'remove_winner', or 'keep_winner'

This exception is raised when the on_end_action condition is not in the list provided
above. These are the only actions available at this time.

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

Use `0` or `false` to disable this condition.

**Arguments:**
    - `<raffle>` - The name of the raffle.
    - `<end_message>` - The new ending message.

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

Clear the prevented list for a raffle.


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
