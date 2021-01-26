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

Cogs labelled with [Dev branch] have been moved there for a reason. They are either still in development, need rewriting, or a major
flaw has been issued. Use these cogs at you're own risk, you're on your own if you make that choice.

+-----------------+--------------------------------------------------------------+---------+----------+
| Cog Name        | Description                                                  | Tags    | Author   |
+=================+==============================================================+=========+==========+
| advanceduptime  | Uptime but with additional statistics and inside an embed.   | Tools   | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| bankthief       | Rob other people's bank accounts, win cash.                  | Economy | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| edition         | Inspired by Twentysix Edition at Red.                        | Fun     | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| higherorlower   | Play the classic higher or lower cards game.                 | Fun     | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| namegenerator   | Generate random names will optional gender arguments.        | Fun     | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| pingoverride    | Replace "Pong." with your own response!                      | Tools   | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| publishcogs     | Publish your new cogs to a channel.                          | Tools   | Kreusada |
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
