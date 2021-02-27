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
| staff           | Alert staff for inconspicuous activity.                      | Mod     | Kreusada |
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
* Status: Rejected - I will not be making changes to this feature.
* Status: Triage Requested - This issue has not yet been reviewed or opened.
* Status: Withdrawn - Withdrawn from action.

**Type Labels**

Each issue or PR **must** have a type label (so that I can keep organised lol)

* Type: Breaking Change - The outlined changes could potentially be breaking to other aspects of the cog.
* Type: Bug - This is a bug report.
* Type: Dev - For the dev branch (currently stale)
* Type: Docs - For documentation (currently infeasible)
* Type: Enhancement - This is an enhancement/feature.
