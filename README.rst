===================================================
Redbot cogs for Red-DiscordBot authored by Kreusada
===================================================

This is my repository for Red Discord-Bot. I built these cogs because these were the features that I wanted for my bot, `WALL-E. <https://discord.com/oauth2/authorize?client_id=766580519000473640&scope=bot&permissions=8>`_

These cogs have been approved by the Red-DiscordBot QA team.

------------
Installation
------------

Primarily, make sure you have `downloader` loaded. 

.. code-block:: ini

    [p]load Downloader

Next, let's add my repository to your system.

.. code-block:: ini

    [p]repo add kreusadacogs https://github.com/kreusada/kreusadacogs

To install a cog, use this command, replacing <cog> with the name of the cog you wish to install:

.. code-block:: ini

    [p]cog install kreusadacogs <cog>

-------------------
Available cogs list
-------------------

+-----------------+--------------------------------------------------------------+---------+----------+
| Cog Name        | Description                                                  | Tags    | Author   |
+=================+==============================================================+=========+==========+
| advanceduptime  | Uptime but with additional statistics and inside an embed.   | Tools   | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| bubblewrap      | Get some bubblewrap.                                         | Fun     | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| codify          | Get messages and transform them into code blocks.            | Tools   | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| dehoister       | Dehoist new users with a variety of powerful tools.          | Mod     | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| edition         | Inspired by Twentysix Edition at Red.                        | Fun     | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| namegenerator   | Generate random names will optional gender arguments.        | Fun     | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| pinginvoke      | r2d2? wall-e? Invoke ping by asking if your bot's there.     | Tools   | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| pingoverride    | Replace "Pong." with your own response!                      | Tools   | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| ram             | Get your bot's random access memory.                         | Tools   | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| sendcards       | Send christmas, birthday, valentines and get well soon cards | Fun     | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| staff           | Alert staff for   conspicuous activity.                      | Mod     | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| textmanipulator | Manipulate text and words with tools.                        | Tools   | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| timestables     | Learn your times tables with an 'against the clock' game.    | Fun     | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| votechannel     | Designate a channel to add voting reactions (customizable).  | Tools   | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+

------------
Contributing
------------

Feel free to open a pull request, or an issue, I'm more than happy to make changes to my work.

-------
Support
-------

Mention me in the #support_othercogs in the `cog support server <https://discord.gg/GET4DVk>`_ if you need any help.

If you're have an important issue(s), open an issue or pull request to this repo.
You can also join my `support server <https://discord.gg/JmCFyq7>`_.

-------
Credits
-------

* Jojo - Got me started with python, and helped me a lot in my early stages.
* Sauri - Learnt how to use `bot.wait_for` via your application cog.
* Flare - Learnt from his userinfo cog, how to replace a command in core, and then add it back on cog unload.
* Trusty - Using reading from json in cog setup files.
* Tobotimus - Lots of backend support.
* Red-DiscordBot - An amazing community, some features have been modified from their repo to use here.
* W3Schools - An amazing website full of python tricks and tips which have helped me out many times.
* Stack Overflow - Of course, I mean who hasn't payed a trip to stack overflow?

-------------
GitHub Labels
-------------

**Category Labels**

* Category: Meta - Related to my repo such as files in ``.github``.
* Category: Internationalization - Related to Internationalization and locales.

**Cog Labels**

Each cog has it's own label to show if the cog has had changes to. 

**Status Labels**

Each issue or PR **must** have a status label (so that I can keep organised lol)

* Status: Admin - Covered by Kreusada, this would normally be for meta.
* Status: Expansive - This issue/PR has had more ideas from the original idea.
* Status: Infeasible - Invalid/off topic.
* Status: Lamented - Died out or behind schedule in accordance to it's milestone/project.
* Status: Passed - PR/Issue has been successfully resolved or has received positive reviews.
* Status: Processing - This PR/Issue is being processed.
* Status: Progress - This PR/Issue is in progress.
* Status: Rejected - I will not be making changes to this feature.
* Status: Requested Changes - Requested changes to this PR. (PR only)
* Status: Triage Requested - This issue has not yet been reviewed or opened.
* Status: Withdrawn - Withdrawn from action.

Additional info:

The lamented label basically means that I really want to get this done, but I aimed for a 
previous milestone which I did not get round to doing. 

There is more information on these labels in accordance with my project workflow in the 
project workflow section of this README.

**Type Labels**

Each issue or PR **must** have a type label (so that I can keep organised lol)

* Type: Breaking Change - The outlined changes could potentially be breaking to other aspects of the cog.
* Type: Bug - This is a bug report.
* Type: Dev - For the dev branch (currently stale)
* Type: Docs - For documentation (currently infeasible)
* Type: Enhancement - This is an enhancement/feature.

**Doclog Labels**

I write and maintain documentation for all of my code on this repository.
There are four Doclog labels which help me to differentiate between entries.

* Doclog: Added - This change has been added to the documentation.
* Doclog: Bypassed - This change does not need to be documented.
* Doclog: Infeasible - This change is invalid and will not be documented.
* Doclog: Pending - This change will be added to the documentation.

----------------
Project Workflow
----------------

I like to add my issues and PRs to my project named 'Workflow',
it helps to keep track of everything I need to get through.

There are four sections:

* To do
* In progress
* Done
* Rejected/Infeasible

If your issue/PR is in the ``To do`` section, that means that I haven't
started looking at it. The issue/PR will have one of the following status labels:

* Status: Lamented
* Status: Processing
* Status: Triage Requested
* Status: Requested Changes (PR Only)

If your issue/PR is in the ``In progress`` section, that means that I have started to 
outline, test or develop the requested changes. The issue/PR will have one of the following status labels:

* Status: Admin
* Status: Progress

If your issue/PR is in the ``Done`` section, that means the requested changes have been implemented or merged!
The issue/PR will have one of the following status labels:

* Status: Passed

If your issue/PR is in the ``Rejected/Infeasible`` section, that means I am not making changes.
The issue/PR will have one of the following status labels:

* Status: Rejected
* Status: Infeasible
* Status: Withdrawn

There is one more status label which hasn't been mentioned yet, which is ``Status: Expansive``.
In order to have this label added, the initial changes must have the ``Status: Passed`` label.
When the PR/issue has passed, and there are additional requested changes, the issue/PR will
move back down to ``To do``, or ``In progress``, where it will continue its development with
the expansive label.

Please avoid elaborating profusely on original issues/PRs with outlined changes. I would much prefer
it that you opened a new issue/PR with the requested changes, so that we won't even need to use the 
expansive label.

----------
Milestones
----------

I have milestones named after months of the year, followed by the year itself.
This helps me to get my work done as soon as possible, aiming to hit the milestones that I add
to the issue/PR. It also gives you an indication of when your issue/PR will be merged.

If the milestone ``February 2020`` was added to your issue/PR, that means I want to get this
implemented or merged BEFORE March 2020.

**Failing to meet milestone deadlines**

In the event that I fail to implement or merge the issue/pr to a sufficient level 
before the deadline ends, you will receive one of two labels:

* Status: Lamented
* Status: Rejected

I have failed to meet the deadline for the following reasons:

1. I'm not 100% certain about this PR/Issue.
2. The requested changes could change the functionality of the cog.
3. I'm very busy and don't have a lot of time to review your issue/PR.
4. The requested changes are complicated, and has therefore taken too long to complete.

If I no longer want to work on the issue/PR, I will simply add the ``Status: Rejected`` label.
If I want to continue work on this issue/PR, I will add the ``Status: Lamented`` label. This
basically means it will be moved back to the ``To do`` project section until I am ready to start
actively working on the issue/PR.

-------
LICENSE
-------

This repository and its cogs are registered under the MIT License.

For further information, please click `here <https://github.com/kreusada/Kreusada-Cogs/blob/master/LICENSE>`_

Copyright (c) 2021 kreusada

==========
Cog Guides
==========

The rest of this space will be filled with cog guides that I've written for my cogs.

Throughout this documentation, ``[p]`` is considered as your prefix.

.. _advanceduptime:

===============
Advanced Uptime
===============

This is the cog guide for the advanceduptime cog. You will
find detailed docs about usage and commands.

Throughout this documentation, ``[p]`` is considered as your prefix.

-----
Usage
-----

This cog is going to show your bot's uptime, with extra information and stats about the bot.

.. _advanceduptime-commands:

--------
Commands
--------

Here's a list of all commands available for this cog.

.. _advanceduptime-command-uptime:

^^^^^^
uptime
^^^^^^

**Syntax**

.. code-block:: ini

    [p]uptime

**Description**

Shows your bot's uptime and additional stats.

You might be wondering, how are you able to use a new uptime command if one already exists in core?
This cog will replace the core uptime command, and then will add the core uptime command back 
if the :code:`AdvancedUptime` cog is unloaded/uninstalled.

This command's output will provide information on your bot's uptime, your bot's name,
your bot's owner (you), the current discord guild, the number of guilds the bot is present in,
the number of unique users your bot has, and the number of commands available!

=========
Dehoister
=========

This is the cog guide for the dehoister cog. You will
find detailed docs about usage and commands.

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

.. _bubblewrap:

==========
Bubblewrap
==========

This is the cog guide for the bubblewrap cog. You will
find detailed docs about usage and commands.

-----
Usage
-----

This cog is going to return spoilers with ``pop`` inside them, so that you can metaphorically pop bubblewrap!

.. _bubblewrap-commands:

--------
Commands
--------

Here's a list of all commands available for this cog.

.. _bubblewrap-command-bubblewrap:

^^^^^^^^^^
bubblewrap
^^^^^^^^^^

**Syntax**

.. code-block:: ini

    [p]bubblewrap

**Description**

This command will return 49 'bubbles' (7x7). These 'bubbles' are actually just the word 
'pop', in spoilers. When you click on these spoilers, the word ``pop`` appears.

.. _codify:

======
Codify
======

This is the cog guide for the codify cog. You will
find detailed docs about usage and commands.

-----
Usage
-----

This cog is going to return spoilers with ``pop`` inside them, so that you can metaphorically pop bubblewrap!

.. _codify-commands:

--------
Commands
--------

Here's a list of all commands available for this cog.

.. _codify-command-codify:

^^^^^^
codify
^^^^^^

**Syntax**

.. code-block:: ini

    [p]codify <message_id> [language=python] [escape_markdown=False]

**Description**

Get a message and wrap it in a codeblock.

**Arguments**

* ``<message_id>``: The message's ID to convert into a codeblock.
* ``[language]``: The language of the codeblock. If none is provided, it defaults to python.
* ``[escape_markdown]``: Determines whether to escape the ``<message_id>``. If none is provided, it defaults to False.

.. _namegenerator:

=============
NameGenerator
=============

This is the cog guide for the namegenerator cog. You will
find detailed docs about usage and commands.

------------
Requirements
------------

* ``names``

This cog requires the ``names`` module, so you will need to pip install it.
Downloader will attempt to do this for you when you install the cog, so please
don't worry about it.

-----
Usage
-----

This cog generates random names, with optional gender arguments.

.. _namegenerator-commands:

--------
Commands
--------

Here's a list of all commands available for this cog.

.. _namegenerator-command-name:

^^^^
name
^^^^

**Syntax**

.. code-block:: ini

    [p]name

**Description**

Commands with namegenerator.

.. _namegenerator-command-name-first:

""""""""""
name first
""""""""""

**Syntax**

.. code-block:: ini

    [p]name first [gender]

**Description**

Generates a random first name.

**Arguments**

* ``[gender]``: The gender for the name. If none is specified, it defaults to random.

.. _namegenerator-command-name-first:

"""""""""
name full
"""""""""

**Syntax**

.. code-block:: ini

    [p]name full [gender]

**Description**

Generates a random full name.

**Arguments**

* ``[gender]``: The gender for the name. If none is specified, it defaults to random.

.. _namegenerator-command-name-last:

""""""""""
name first
""""""""""

**Syntax**

.. code-block:: ini

    [p]name last [gender]

**Description**

Generates a random last name.

**Arguments**

* ``[gender]``: The gender for the name. If none is specified, it defaults to random.

.. _pinginvoke:

==========
PingInvoke
==========

This is the cog guide for the pinginvoke cog. You will
find detailed docs about usage and commands.

-----
Usage
-----

This cog will invoke the ping command by asking if your bot is there.

For instance, if your bot was called WALL-E, whenever I say "walle?", 
it will invoke the ping command. This can be set to whatever you want, as long as it ends in a question mark.

.. tip::

    This cog works amazingly with my PingOverride cog! I suggest you install that too (not required, suggested).

.. _pinginvoke-commands:

--------
Commands
--------

Here's a list of all commands available for this cog.

.. _pinginvoke-command-pingi:

^^^^^
pingi
^^^^^

**Syntax**

.. code-block:: ini

    [p]pingi

**Description**

Commands to configure PingInvoke.

.. _pinginvoke-command-pingi-reset:

"""""""""""
pingi reset
"""""""""""

**Syntax**

.. code-block:: ini

    [p]pingi reset

**Description**

Resets and disables PingInvoke. Your bot will no longer respond if you 
call for it.

.. _pinginvoke-command-pingi-set:

"""""""""
pingi set
"""""""""

**Syntax**

.. code-block:: ini

    [p]pingi set <botname>

**Description**

Sets the botname to respond to. This is case insensitive.
For example, if you used ``[p]pingi set walle``, and then you said
"walle?", it would invoke the ping command.

.. note:: There is no need to include the question mark in ``<botname>``.

**Arguments**

* ``<botname>``: The name to listen for.

.. _pinginvoke-command-pingi-settings:

""""""""""""""
pingi settings
""""""""""""""

**Syntax**

.. code-block:: ini

    [p]pingi settings

**Description**

Shows the settings for PingInvoke.

.. _pingoverride:

============
PingOverride
============

This is the cog guide for the pingoverride cog. You will
find detailed docs about usage and commands.

-----
Usage
-----

This cog will allow you to customize the response from the ``ping`` command.
So instead of "Pong.", it could be "Beep boop.", or whatever you want!

.. note:: 

    This cog replaces the core's ``ping`` command. If you wish to have the old ping command
    back, you can simply unload this cog.

.. tip::

    This cog works amazingly with my PingInvoke cog! I suggest you install that too (not required, suggested).

.. _pingoverride-commands:

--------
Commands
--------

Here's a list of all commands available for this cog.

.. _pingoverride-command-ping:

^^^^
ping
^^^^

**Syntax**

.. code-block:: ini

    [p]ping

**Description**

Pong? Or not?

Replies with all the PingOverride settings, and your configured response.

.. _pinginvoke-command-pingset:

^^^^^^^
pingset
^^^^^^^

**Syntax**

.. code-block:: ini

    [p]pingset

**Description**

Commands to configure PingOverride. Settings include:

* Embed send
* Replies
* Reply mentions
* Response with special regex

.. _pinginvoke-command-pingset-embed:

^^^^^^^^^^^^^
pingset embed
^^^^^^^^^^^^^

**Syntax**

.. code-block:: ini

    [p]pingset embed <true_or_false>

**Description**

Sets whether the response is sent inside an embed.
On cog install, this setting is false.

.. note:: If the bot doesn't have permissions to send embeds, this setting will be bypassed.

**Arguments**

* ``<true_or_false>``: Toggle for embeds setting. Must specify ``true`` or ``false``.

.. _pinginvoke-command-pingset-message:

^^^^^^^^^^^^^^^
pingset message
^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: ini

    [p]pingset message <response>

**Description**

Set the message that is sent via the ``ping`` command.

Example Usage: ``[p]pingset message Hello {display}! My latency is {latency} ms.``

**Response Regex**

* ``{display}`` - Replaced with the author's display name.
* ``{latency}`` - Replaces with the bot's latency.

**Arguments**

* ``<response>``: The message that is sent via the ``ping`` command.

.. _pinginvoke-command-pingset-reply:

^^^^^^^^^^^^^
pingset reply
^^^^^^^^^^^^^

**Syntax**

.. code-block:: ini

    [p]pingset reply <true_or_false> [mention=False]

**Description**

Toggles whether the ping response will use Discord replies. 
Additionally, you can toggle this to mention, or not.

**Arguments**

* ``<true_or_false>``: Toggle for the replies setting. Must specify ``true`` or ``false``.
* ``[mention=False]``: Toggle whether replies will mention. Specify ``true`` or ``false``. Defaults to False.

.. _pinginvoke-command-pingset-settings:

^^^^^^^^^^^^^^^^
pingset settings
^^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: ini

    [p]pingset settings

**Description**

Shows the settings for PingOverride.

.. _ram:

==========================
RAM (Random Access Memory)
==========================

This is the cog guide for the ram cog. You will
find detailed docs about usage and commands.

-----
Usage
-----

This cog will display your client's RAM usage.

.. _ram-commands:

--------
Commands
--------

Here's a list of all commands available for this cog.

.. _ram-command-ram:

^^^
ram
^^^

**Syntax**

.. code-block:: ini

    [p]ram

**Description**

Displays your client's RAM usage as a percentage, as well as scaled.

.. _sendcards:

=========
SendCards
=========

This is the cog guide for the sendcards cog. You will
find detailed docs about usage and commands.

-----
Usage
-----

This cog allows you to send cards to other users in DMs.

.. _sendcards-commands:

--------
Commands
--------

Here's a list of all commands available for this cog.

.. _sendcards-command-send:

^^^^
send
^^^^

**Syntax**

.. code-block:: ini

    [p]send

**Description**

Commands with sendcards.

.. warning:: 

    When the birthday card is sent, we already add the recipients in the card for you.
    Please consider this to improve your card sending and to avoid repetition.

    Dear User,

    ``YOUR MESSAGE WILL GO HERE``

    From Your Name

.. _sendcards-command-send-birthday:

^^^^^^^^^^^^^
send birthday
^^^^^^^^^^^^^

**Syntax**

.. code-block:: ini

    [p]send birthday <user_id> <message>

**Description**

Send someone a birthday card.

**Arguments**

* ``<user_id>``: The ID of the user to send this card to.
* ``<message>``: The message you want to send to the user.

.. _sendcards-command-send-christmas:

^^^^^^^^^^^^^^
send christmas
^^^^^^^^^^^^^^

**Syntax**

.. code-block:: ini

    [p]send christmas <user_id> <message>

**Description**

Send someone a christmas card.

**Arguments**

* ``<user_id>``: The ID of the user to send this card to.
* ``<message>``: The message you want to send to the user.

.. _sendcards-command-send-getwellsoon:

^^^^^^^^^^^^^^^^
send getwellsoon
^^^^^^^^^^^^^^^^

**Syntax**

.. code-block:: ini

    [p]send getwellsoon <user_id> <message>

**Description**

Send someone a getwellsoon card.

**Arguments**

* ``<user_id>``: The ID of the user to send this card to.
* ``<message>``: The message you want to send to the user.

.. _sendcards-command-send-valentine:

^^^^^^^^^^^^^^
send valentine
^^^^^^^^^^^^^^

**Syntax**

.. code-block:: ini

    [p]send valentine <user_id> <message>

**Description**

Send someone a valentine card.

**Arguments**

* ``<user_id>``: The ID of the user to send this card to.
* ``<message>``: The message you want to send to the user.

.. _staff:

=====
Staff
=====

This is the cog guide for the staff cog. You will
find detailed docs about usage and commands.

-----
Usage
-----

This will allow you to alert staff for conspicuous activity.

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

Alert the staff for conspicuous activity.

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

.. _staff-command-staffset-channel:

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

.. _textmanipulator:

===============
TextManipulator 
===============

This is the cog guide for the textmanipulator cog. You will
find detailed docs about usage and commands.

-----
Usage
-----

Manipulate text with tools.

.. _textmanipulator-commands:

--------
Commands
--------

Here's a list of all commands available for this cog.

.. _textmanipulator-command-convert:

^^^^^^^
convert
^^^^^^^

**Syntax**

.. code-block:: ini

    [p]convert

**Description**

Convert text to different casetypes or change their UI.

.. _textmanipulator-command-convert-alt:

"""""""""""
convert alt
"""""""""""

**Syntax**

.. code-block:: ini

    [p]convert alt <characters>

**Description**

Convert text to AlTeRnAtInG cAsE.

**Arguments**

* ``<characters>``: The text to convert.

.. _textmanipulator-command-convert-lower:

"""""""""""""
convert lower
"""""""""""""

**Syntax**

.. code-block:: ini

    [p]convert lower <characters>

**Description**

Convert text to lower case.

**Arguments**

* ``<characters>``: The text to convert.

.. _textmanipulator-command-convert-snake:

"""""""""""""
convert snake
"""""""""""""

**Syntax**

.. code-block:: ini

    [p]convert snake <characters>

**Description**

Convert text to have_snake_spaces.

**Arguments**

* ``<characters>``: The text to convert.

.. _textmanipulator-command-convert-title:

"""""""""""""
convert title
"""""""""""""

**Syntax**

.. code-block:: ini

    [p]convert title <characters>

**Description**

Convert text to Title Case.

**Arguments**

* ``<characters>``: The text to convert.

.. _textmanipulator-command-convert-upper:

"""""""""""""
convert upper
"""""""""""""

**Syntax**

.. code-block:: ini

    [p]convert upper <characters>

**Description**

Convert text to UPPER CASE.

**Arguments**

* ``<characters>``: The text to convert.

.. _textmanipulator-command-count:

^^^^^
count
^^^^^

**Syntax**

.. code-block:: ini

    [p]count

**Description**

Count the number of characters/words in text.

.. _textmanipulator-command-count-characters:

""""""""""""""""
count characters
""""""""""""""""

**Syntax**

.. code-block:: ini

    [p]count characters <characters>

**Description**

Count the number of characters in the text.

**Arguments**

* ``<characters>``: The text to count against.

.. _textmanipulator-command-count-characters:

"""""""""""
count words
"""""""""""

**Syntax**

.. code-block:: ini

    [p]count words <words>

**Description**

Count the number of words in the text.

**Arguments**

* ``<words>``: The text to count against.

.. _textmanipulator-command-escape:

^^^^^^
escape
^^^^^^

**Syntax**

.. code-block:: ini

    [p]cscape <words>

**Description**

Escape Discord markdown in the text.

**Arguments**

* ``<words>``: The text to escape.

.. _textmanipulator-command-remove:

^^^^^^
remove
^^^^^^

**Syntax**

.. code-block:: ini

    [p]remove <char_to_remove> <words>

**Description**

Remove a specific character from the text.

**Arguments**

* ``<char_to_remove>``: The character to remove.
* ``<words>``: The text to remove this character from.

.. _timestables:

===========
TimesTables
===========

This is the cog guide for the timestables cog. You will
find detailed docs about usage and commands.

-----
Usage
-----

This cog will allow you to practice your timestables up to 12x12, with stats such as correct, incorrect,
unanswered questions, average time per question, and total time for all questions.

.. _timestables-commands:

--------
Commands
--------

Here's a list of all commands available for this cog.

.. _timestables-command-tt:

^^
tt
^^

**Syntax**

.. code-block:: ini

    [p]tt

**Description**

Base command for timestables.

.. _timestables-command-tt-inactive:

"""""""""""
tt inactive
"""""""""""

**Syntax**:

.. code-block:: ini

    [p]tt inactive <questions>

**Description**

Set the number of questions unanswered before the session is automatically
closed due to inactivity.

**Arguments**

* ``<questions>``: The number of questions before the session ends due to inactivity.

.. _timestables-command-tt-settings:

"""""""""""
tt settings
"""""""""""

**Syntax**:

.. code-block:: ini

    [p]tt settings

**Description**

Shows the current settings for times tables.

.. _timestables-command-tt-sleep:

""""""""
tt sleep
""""""""

**Syntax**:

.. code-block:: ini

    [p]tt sleep <seconds>

**Description**

Set the number of seconds between each question.

**Arguments**

* ``<seconds>``: The number of seconds to sleep between each question in seconds.

.. _timestables-command-tt-start:

""""""""
tt start
""""""""

**Syntax**:

.. code-block:: ini

    [p]tt start <number_of_questions>

**Description**

Start playing the timestables game!

**Arguments**

* ``<number_of_questions>``: The number of questions in the round.

.. _timestables-command-tt-time:

"""""""
tt time
"""""""

**Syntax**:

.. code-block:: ini

    [p]tt time

**Description**

Toggles whether time is recorded when you play timestables.

.. _timestables-command-tt-timeout:

"""""""
tt timeout
"""""""

**Syntax**:

.. code-block:: ini

    [p]tt timeout <seconds>

**Description**

Sets how long you have to answer each question.

**Arguments**

* ``<seconds>``: The length of time per question in seconds.

===========
VoteChannel
===========

This is the cog guide for the votechannel cog. You will
find detailed docs about usage and commands.

-----
Usage
-----

Designate multiple channels to have poll emojis reacted to each
message sent in them.

.. _votechannel-commands:

--------
Commands
--------

Here's a list of all commands available for this cog.

.. _votechannel-command-vote:

^^^^
vote
^^^^

**Syntax**

.. code-block:: ini

    [p]vote

**Description**

Commands with votechannel.

.. _votechannel-command-vote-channel:

""""""""""""
vote channel
""""""""""""

**Syntax**

.. code-block:: ini

    [p]vote channel

**Description**

Settings for channels.

.. _votechannel-command-vote-channel-add:

""""""""""""""""
vote channel add
""""""""""""""""

**Syntax**

.. code-block:: ini

    [p]vote channel add <channel>

**Description**

Add a channel to the votechannel list.

**Arguments**

* ``<channel>``: The Discord channel to receive poll reactions for each message sent inside it.

.. _votechannel-command-vote-channel-remove:

"""""""""""""""""""
vote channel remove
"""""""""""""""""""

**Syntax**

.. code-block:: ini

    [p]vote channel remove <channel>

**Description**

Remove a channel from the votechannel list.

**Arguments**

* ``<channel>``: The Discord channel to remove from the votechannel list.

.. _votechannel-command-vote-channel-list:

"""""""""""""""""
vote channel list
"""""""""""""""""

**Syntax**

.. code-block:: ini

    [p]vote channel list

**Description**

List the current voting channels.

.. _votechannel-command-vote-emoji:

""""""""""
vote emoji
""""""""""

**Syntax**

.. code-block:: ini

    [p]vote emoji

**Description**

Set and view the current emojis used for votechannel.

.. _votechannel-command-vote-emoji-down:

"""""""""""""""
vote emoji down
"""""""""""""""

**Syntax**

.. code-block:: ini

    [p]vote emoji down [emoji]

**Description**

Sets the downvote emoji for votechannel.

**Arguments**

* ``[emoji]``: The emoji to react with.

.. _votechannel-command-vote-emoji-down:

"""""""""""""
vote emoji up
"""""""""""""

**Syntax**

.. code-block:: ini

    [p]vote emoji up [emoji]

**Description**

Sets the upvote emoji for votechannel.

**Arguments**

* ``[emoji]``: The emoji to react with.

.. _votechannel-command-vote-emoji-presets:

""""""""""""""""""
vote emoji presets
""""""""""""""""""

**Syntax**

.. code-block:: ini

    [p]vote emoji presets

**Description**

Shows the current emojis used for votechannel.

.. _votechannel-command-vote-toggle:

"""""""""""
vote toggle
"""""""""""

**Syntax**

.. code-block:: ini

    [p]vote toggle

**Description**

Toggle votechannel.
