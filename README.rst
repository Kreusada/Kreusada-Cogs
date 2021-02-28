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

Check out my docs `here <https://kreusadacogs.readthedocs.io/en/latest/>`_

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
