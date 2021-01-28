===================================================
Redbot cogs for Red-DiscordBot authored by Kreusada
===================================================

This is my repository for Red Discord-Bot. I built these cogs because these were the features that I wanted for my bot, `WALL-E. <https://discord.com/oauth2/authorize?client_id=766580519000473640&scope=bot&permissions=8>`_

------------
Installation
------------

Primarily, make sure you have `downloader` loaded. 

.. code-block:: ini

    [p]load Downloader

Next, let's add my repository to your system.

.. code-block:: ini

    [p]repo add kreusadacogs https://github.com/kreus7/kreusadacogs

Finally, you can load cogs from my repo by executing the following command:

.. code-block:: ini

    [p]cog install kreusadacogs <cog>

Remember - don't include the `<>` when you use this command. Those characters are just to show you where to enter the cog name.

-------------------
Available cogs list
-------------------

+-----------------+--------------------------------------------------------------+---------+----------+
| Cog Name        | Description                                                  | Tags    | Author   |
+=================+==============================================================+=========+==========+
| advanceduptime  | Uptime but with additional statistics and inside an embed.   | Tools   | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| codify          | Get messages and transform them into code blocks.            | Tools   | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| edition         | Inspired by Twentysix Edition at Red.                        | Fun     | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| higherorlower   | Play the classic higher or lower cards game.                 | Fun     | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| namegenerator   | Generate random names will optional gender arguments.        | Fun     | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| pingoverride    | Replace "Pong." with your own response!                      | Tools   | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| ram             | Get your bot's random access memory.                         | Tools   | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| romanconverter  | Convert to roman numerals, and vise versa.                   | Tools   | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| searchengine    | Search Google, Pinterest or Redbubble.                       | Tools   | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| sendcards       | Send christmas, birthday, valentines and get well soon cards | Fun     | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| staff           | Alert staff for inconspicuous activity.                      | Mod     | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| textmanipulator | Manipulate text and words with tools.                        | Tools   | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+

--------
Support
--------

If you're having any important issue(s), open an issue or pull request to this repo.
Join my `support server <https://discord.gg/JmCFyq7>`_.

--------
Credits
--------

* Jojo - Got me started with python, and helped me a lot in my early stages.
* Sauri - Learnt how to use `bot.wait_for` via your application cog.
* Flare - Learnt from his userinfo cog, how to replace a command in core, and then reverse those changes on unload.
* Tobotimus - Lots of kind and motivational words to help my progression as a developer. 

==========
Cog Guides
==========

A few cog guides are ready to help you understand how my cogs work!

===============
Higher Or Lower
===============

-------
Outline
-------

Higher or Lower is a standard card game which involves arbitrarily selecting a random card subsequent to your current card.
If you correctly guess that the next card is 'higher' or 'lower' than your current card, you advance to the next card.

In a standard game, there would be nine cards to arbitrarily advance through. This cog also has the default number of cards (9), 
but can be modified to your guild's liking via the :code:`[p]holset` command.

-----
Usage
-----

* :code:`[p]hol`

:code:`hol`, as you may have guessed, stands for 'Higher Or Lower'! This command will allow you to start a game session with the guild's 
current features.

-----
Setup
-----

Setup is absolutely not required; if you want to keep things completely normal, you can start playing right away! 
However, customization is great, so there are a few settings that you can change to your GUILD's liking.
These settings are per guild to allow more customization for particular tastes in user interface and difficulty.
There are also settings per user which helps make your user's experience even greater!

.. code-block:: ini

  [p]holset image <bool>
  
This command allows you to set whether you would like the card image to be small, as a thumbnail, or large, as a full image.
Personally, I prefer having a smaller thumbnail, which is why I added both options. Images are great for desktop, whereas when you're 
on mobile, thumbnails are more appropriate for the smaller screen.

.. note:: This command is a setting personal to you, meaning that no one can change it except yourself.

This command is known as a boolean, meaning that you must specify either :code:`true` or :code:`false` after :code:`[p]holset image`.

.. code-block:: ini

  [p]holset total <int>
  
This command is locked to moderators or administrators, this setting will apply for everyone in your guild.
:code:`<int>` stands for integer. Here, you need to specify an integer which will determine the total number of 
cards your guild members have to work through to win.

.. attention:: 

  To be courteous to users, we've set a limit for this command.
  You cannot specify an integer less than 4, or greater than 20.
  
.. code-block:: ini

  [p]holset togglebank <bool>
  
This command is locked to moderators or administrators.
This command allows users to receive credits for each card they answer, or each round they complete. On installation, this setting's 
default is off. You must specify either :code:`true` or :code:`false`, if not, the boolean will default to :code:`false`.

Although you may have enabled the bank, the per card, and per round payouts default to zero. See the usage below to help configure these values.

.. warning::

  For these commands, **bank must be loaded.**
  
.. code-block:: ini

  [p]holset perpayout
  
This command is locked to moderators or administrators.
Sets the amount of credits that a user will receive per card that they correctly answer. On installation, this setting's default is 0.
The bank must be loaded through :code:`[p]load bank`, and it must be enabled via :code:`[p]holset togglebank true`, for transactions to take place.
You cannot specify a deposit above 1000.

.. code-block:: ini

  [p]holset roundpayout
  
This command is locked to moderators or administrators.
Sets the amount of credits that a user will receive per round that they complete. On installation, this setting's default is 0.
The bank must be loaded through :code:`[p]load bank`, and it must be enabled via :code:`[p]holset togglebank true`, for transactions to take place.
You cannot specify a deposit above 100000.

===============
Advanced Uptime
===============

-------
Outline
-------

This cog is going to show your bot's uptime, with extra information and stats.

-----
Usage
-----

* :code:`[p]uptime`

You might be wondering, how are you able to use a new uptime command if one already exists?
This cog will replace the core uptime command, and then will add the core uptime command back 
if the :code:`AdvancedUptime` cog is unloaded/uninstalled.

This command's output will provide information on your bot's uptime, your bot's name,
your bot's owner (you), the current discord guild, the number of guilds the bot is present in,
the number of unique users your bot has, and the number of commands available!

===============
Ping Override
===============

--------
Overview
--------

PingOverride is a cog which allows you to override/overwrite the core's ping command with your own customisable response. This means that you can replace the "Pong." response, with something of your choosing. There are also additional options such as saying the author's name, and showing the bot latency. 

--------
Commands
--------

.. code-block:: ini
  
  [p]ping

This command is going to print the response which you requested for using [p]pingset.

.. code-block:: ini

  [p]pingset

Here, you can set the ping response. There are additional options you can use such as:

:code:`{latency}` - Provides the bot's latency.

:code:`{name}` - Returns the author's display name.

**Example setup**

.. code-block:: python

  [p]pingset Hello {name}! My latency is currently at {latency} ms.

  [p]pingset Beep boop.
  
==========
Staff
==========

-------
Outline
-------

The ``staff`` cog is a cog used to alert the staff. It's that simple. This cog guide will give you the setup instructions.

-----------
Staff Setup
-----------

**Setting your staff role**

Staff roles are required to notify your staff.

.. code-block:: none 

      [p]staffset role <role>

When the staff command is used, this configured role will be mentioned, allowing for staff to be notified straight away.

**Setting your staff channel**

Set your staff channel to a private mod/admin channel. 

.. code-block:: none

      [p]staffset role <role>

When the staff command is used, this configured channel host a message containing the alert, the mention, the location of which the ``staff`` command was used, and the user who executed the command.

^^^^^^^^^^^
Staff Usage
^^^^^^^^^^^

**Syntax**

.. code-block:: none

     [p]staff
     
================
PublishCogs
================

.. attention:: 

	PublishCogs has now been moved to the Dev branch. Feel free to use it, however,
	the code is faulty and I recognise that on my end. Multiple sessions could start, and
	although it could be a quick fix, I still need to rewrite the full cog anyway.

	Please use PublishCogs at your own risk, you're on your own if you make that choice.
	The docs should help you out but I won't be giving support for this cog until its back on master.

	Additionally, if you would like to create a PR on the dev branch, feel free.

-------
Outline
-------

:code:`PublishCogs` is a cog which allows you to publish your new cogs to a specific channel in your guild! With a fully customizable output, you can set your new cogs to only display the author and cogname, or the author, cogname, description, pre-requirements, install guide and the current time on your embed's footer! Seems confusing, no? This guide should help you to get an understanding for this cog.

-----
Usage
-----

.. code-block:: ini

	[p]publishcog

Publishes cogs to a channel with a few questions to fill out first.

.. attention:: Setting your channel and cog creator role is a must before using these commands. Please contact an admin.

.. note:: Only Cog Creators will be able to use this command.

-----------
Setup Usage
-----------

.. code-block:: ini

	[p]publishcogset

Configure settings for new cogs.

--------------
Setup: Channel
--------------

.. code-block:: ini

	[p]publishcogset channel <#channel>

.. attention:: This setting is a **requirement** for this cog to work properly.

Set your channel for published cogs to be sent to.

-----------------
Setup: Footerdate
-----------------

.. code-block:: ini

	[p]publishcogset footerdate

This is not a requirement. Running this command will bring you to a yes or no predicate which will determine your settings.

-----------------------
Setup: Cog Creator Role
-----------------------

.. code-block:: ini

	[p]publishcogset cogcreator

.. attention:: This setting is a **requirement** for this cog to work properly.

Only those with the configured cog creator role will be able to use the :code:`[p]publishcog` command.

------------------
Setup: Description
------------------

.. code-block:: ini

	[p]publishcogset description

.. tip:: This setting is not required, but is advised. Otherwise, the cog won't have a description! Unless you want it to remain anonymous, of course.

Sets the ability to add description for published cogs. Running this command will bring you to a yes or no predicate which will determine your settings.

----------------------
Setup: Prerequirements
----------------------

.. code-block:: ini

	[p]publishcogset prerequirements

Sets the ability to add pre-requirements for published cogs. Running this command will bring you to a yes or no predicate which will determine your settings.

--------------------
Setup: Install Guide
--------------------

.. code-block:: ini

	[p]publishcogset installguide

.. tip:: This setting is not required, but is advised. Otherwise, the cog won't have an install guide.

Sets the ability to add an install guide for published cogs. Running this command will bring you to a yes or no predicate which will determine your settings.

--------------
Setup: Set All
--------------

.. code-block:: ini

	[p]publishcogset setall

This command will toggle all toggleable commands on, or off! Running this command will bring you to a yes or no predicate which will determine your settings.
