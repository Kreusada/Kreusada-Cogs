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
| codify          | Get messages and transform them into code blocks.            | Tools   | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| dehoister       | Dehoist new users with higher ASCII.                         | Mod     | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| edition         | Inspired by Twentysix Edition at Red.                        | Fun     | Kreusada |
+-----------------+--------------------------------------------------------------+---------+----------+
| namegenerator   | Generate random names will optional gender arguments.        | Fun     | Kreusada |
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

-------------
Contributing
-------------

Feel free to open a pull request, or an issue, I'm more than happy to make changes to my work.

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
* Flare - Learnt from his userinfo cog, how to replace a command in core, and then add it back on cog unload.
* Trusty - Using JSON for :code:`__init__` files.
* Tobotimus - Lots of backend support.
* Red-DiscordBot - An amazing community, some features have been modified from their repo to use here.
* W3Schools - An amazing website full of python tricks and tips which have helped me develop. 
 You can find their website here: https://www.w3schools.com/python/
* Stack Overflow - Of course, I mean who hasn't payed a trip to stack overflow?

--------------------------
Frequently Asked Questions
--------------------------

**What is your favourite cog that you've created?**

Probably PingOverride. It's been super fun creating it, and I've really
enjoyed providing it with flexibility and making it look good.

**Where did some of your cogs go that were previously on your repo?**

They were removing intentionally because they either had breaking changes or
needed rewriting. They're scattered around somewhere, I won't be giving support 
for them.

**Which cog do you dislike the most?**

TextManipulator. No reason - all the code is correct, but it was just a bit of advanceduptime
'naff' project.

**Why did you start creating cogs?**

I started coding python when my hometown went into lockdown in April 2020. Then, my friend Jojo
mentioned 'Red' to me. I was confused, but I had seen Red around, so decided to talk more about it.
Then I discovered that Red had a server, so I joined, and my first question was 'Is Red discord.js?'.
Since then, I've been able to code cogs, and it's been very fun! I am currently an unnapproved cog
creator, but I have submitted an application on the cogboard on January 2nd.

**Do you maintain your repo?**

Yes. I try my best to check that all cogs work as well as they can.

**Do you maintain your PyPi?**

Not as much as my repo. But I do try.