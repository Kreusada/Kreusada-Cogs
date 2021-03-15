.. _dehoister:

=========
Dehoister
=========

This is the cog guide for the dehoister cog. You will
find detailed docs about usage and commands.

Throughout this documentation, ``[p]`` is considered as your prefix.

------------
Installation
------------

Let's firstly add my repository if you haven't already:

* :code:`[p]repo add kreusada https://github.com/kreusada/kreusadacogs`

Next, let's download the cog from the repo:

* :code:`[p]cog install kreusada dehoister`

Finally, you can see my end user data statements, cog requirements, and other cog information by using:

* :code:`[p]cog info kreusada dehoister`

-----
Usage
-----

Dehoister will protect your guild against users with hoisted usernames. Hoisted names are often used to
promote scams, hate speech, guilds, and other things which may come across as malicious. Or, its just your
average discord user going "I'm at the top of the member list look at me look at meeee!".

This cog will take action on any user, if their name starts with one of `these characters <https://github.com/kreusada/Kreusada-Cogs/blob/master/dehoister/dehoister.py#L40>`_.

They are the only characters that come above numbers and letters in ASCII, and if a user's name starts
with one of these, 90% of the time it will be because they want to be hoisted.

Features include 'scanning and cleaning' and auto-dehoisting, with lots of customization such as the nickname,
and modlog events.

.. _dehoister-commands:

--------
Commands
--------

Here's a list of all commands available for this cog.

.. _dehoister-command-hoist:

^^^^^
hoist
^^^^^

**Syntax**

.. code-block:: ini

    [p]hoist

**Description**

This is the main command used for dehoister.
It will be used for all other commands.

.. _dehoister-command-hoist-clean:

"""""""""""
hoist clean
"""""""""""

**Syntax**

.. code-block:: ini

    [p]hoist clean

**Description**

Dehoist all members in the guild.

.. note:: Your server owner's nickname cannot be changed due to Discord permissions.

.. _dehoister-command-hoist-dehoist:

"""""""""""""
hoist dehoist
"""""""""""""

**Syntax**

.. code-block:: ini

    [p]hoist dehoist <member>

**Description**

Dehoist a particular member.

.. note:: Your server owner's nickname cannot be changed due to Discord permissions.

**Arguments**

* ``<member>``: The member to dehoist.

.. _dehoister-command-hoist-explain:

"""""""""""""
hoist explain
"""""""""""""

**Syntax**

.. code-block:: ini

    [p]hoist explain

**Description**

Explain how Dehoister works.

.. _dehoister-command-hoist-explain-auto:

""""""""""""""""""
hoist explain auto
""""""""""""""""""

**Syntax**

.. code-block:: ini

    [p]hoist explain auto

**Description**

Explain how auto-dehoist works.

To get started, use ``[p]hoist set toggle true``, which will enable this feature. Then, you can customize the nickname via ``[p]hoist set nickname``.
When new users join the guild, their nickname will automatically be changed to this configured nickname, if they have a hoisted character at the start of their name.
If your bot doesn't have permissions, this process will be cancelled, so make sure that your bot has access to nickname changing.

.. _dehoister-command-hoist-explain-scanclean:

"""""""""""""""""""""""
hoist explain scanclean
"""""""""""""""""""""""

**Syntax**

.. code-block:: ini

    [p]hoist explain scanclean

**Description**

Explain how scanning and cleaning works.

If users were able to bypass the auto dehoister, due to the bot being down, or it was toggled off, there are still tools you can use to 
protect your guild against hoisted names. ``[p]hoist scan`` will return a full list of users who have hoisted nicknames or usernames. 
``[p]hoist clean`` will change everyones nickname to the configured nickname if they have a hoisted username/nickname.

.. _dehoister-command-hoist-scan:

""""""""""
hoist scan
""""""""""

**Syntax**

.. code-block:: ini

    [p]hoist scan

**Description**

Scan for hoisted members.

This command will return a count and list of members.
It will follow this format:

---------------------------------

X users found:

user#0001:
- Their nickname (if applicable)
-- Their user ID

user#9999:
- Their nickname (if applicable)
-- Their user ID

---------------------------------

If there are more than 10 hoisted users, this list
will instead be sent as a Discord file, named ``hoisted.txt``.

.. _dehoister-command-hoist-set:

"""""""""
hoist set
"""""""""

**Syntax**

.. code-block:: ini

    [p]hoist set

**Description**

Settings for dehoister.

.. _dehoister-command-hoist-set-nickname:

""""""""""""""""""
hoist set nickname
""""""""""""""""""

**Syntax**

.. code-block:: ini

    [p]hoist set nickname <nickname>

**Description**

Set the nickname which is applied to users with hoisted display names.

This nickname will be referred to everytime this cog takes
action on members with hoisted display names, so make sure you
find a suitable display name!

The default nickname that comes with the cog is ``δ Dehoisted``.

**Arguments**

* ``<nickname>``: The nickname to set to.

.. _dehoister-command-hoist-set-toggle:

""""""""""""""""
hoist set toggle
""""""""""""""""

**Syntax**

.. code-block:: ini

    [p]hoist set toggle

**Description**

Toggle the auto-dehoister from dehoisting users who join the guild with hoisted usernames.
When installed, this setting is FALSE by default.

----------------------
Additional Information
----------------------

This cog has been vetted by the Red-DiscordBot QA team as approved.
For inquiries, see to the contact options below.

---------------
Receive Support
---------------

Feel free to ping me at the `Red Cog Support Server <https://discord.gg/GET4DVk>`_ in :code:`#support_othercogs`,
or you can head over to `my support server <https://discord.gg/JmCFyq7>`_ and ask your questions in :code:`#support-kreusadacogs`.