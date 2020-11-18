.. _v1.1:

Demaratus 2.1 (01/11/2020)
==========================

A massive thankyou to everyone who contributed towards this release.

Additionally, thankyou to our servers who have helped to invoke, bolster its development, and share within the community. Currently, as of 01/11/2020, we have 63164 unique users, in 27 different servers.


Changelog Summary
-----------------

Demaratus 2.1 brings lots of new fun features, vast UI improvements, and improving your user experience. Many issues and bugs have been resolved, and our main focus has been to release roster for ``mcoc``. Unfortunately, we were not able to get it released on time for the version release date, but we are working on adding the finishing touches as we speak. Demaratus 2.1 build has been HUGE, with over 1,000 code commits and approximately 60 hours spent. Below, you will find all the patch notes relative to Demaratus.

This changelog was scripted by Kreusada and Andreas. 

Changelog
---------

- Added our ``battlechip`` command group which uses official DRs from Marvel Contest of Champions.
- Added star ratings to champions in ``crystals``
- Added more ``trivia`` questions to ``pixel`` and ``mcoc``.
- Added redcore categories overtime for ``trivia``.
- Removed ``champ portrait`` and ``champ featured`` as we look to rebuild these cogs.
- Removed static methods, modlog reports, timedelta and datetime modules, and peripheral scars from certain cogs.
- Improved User Interface amongst Kreusada's Cogs.
- Improved Ticket System for UI, improved menus, deprecated ``quicksetup`` for clarity.
- Improved our ``crystal`` functionality with replaced URLs and on the rebuild.
- Greatly improved our user interface for ``dadjokes``.
- Bolstered ``trivia`` response messages.
- Clarified the justification between previous instance versions.
- Investigating the cause and a fix for missing champion featured images in ``crystals``.
- Investigating the cause and a fix for embed spams in certain channel types.
- Investigating the cause and a fix for user trigger messages occassionally being removed when a command timeout is applied to the command group.
- Investigating the cause and a fix for 'laggy' embeds in ``awbadges``.
- Investigating issues relating to server owners having heirarchy higher than Demaratus although Demaratus is higher in the heirarchy.
- Investigating issues relating to multiple ``excepts`` being sent for discord forbidden permission quotas.
- Investigating issues relating to reactmenus in ``awbadges`` becoming 'laggy' and inuniform.
- Fixed issue where embeds were occassionally 'distorted'.
- Fixed issue where embeds were exceeding the max character limit, although they were under the specified amount.
- Fixed issue for certain cogs to no longer falsely clarify the fact that they store user end data.
- Fixed issue where users were unable to use the ``invite`` command although global permissions were granted.
- Fixed issue where hardcoded alliance roleids were displaying roleids instead of rolenames.
- Fixed issue where some embed footers were displaying invalid information.
- Fixed issues relating to ``Audio`` not being able to play YouTube tracks.
- Fixed issues relating to ``Audio`` not making any sound despite audio in queue with full volume.
- Fixed issues relating to ``Audio`` lavalink port 2333 interfering with our other instances.
- Fixed issue where staffset commands were not operating without a configured mod role from ``set addmodrole <role>``. This was not intentional.
- Fixed issue where the parent group command is displaying on top of the group's child commands.
- Fixed issue where commands were not invoked from their parents.
- Fixed issue where the mention attribute is now unclassified in ``alliancealertset showsettings``.

In development
--------------

- Adding drop rates to the newly established tiers.
- Adding authentic rosters for each tier. [Primary Development]
- Adding ``find`` commands into ``mcoc``.
- Editing forks to replace datapath core cogs to better authenticate the branding for Demaratus.

New Cogs
--------

**Alliance**

- Added a ``timezone`` tool to bind to the end of your nickname.

- TBD AQ+AW Alerts for Marvel Contest of Champions. 

**Find**

- Find MCOC PNGs with this quick and accessible tool. [MAINTENANCE]

- ``Find`` is now in the process of being merged from its own cog to ``mcoc``. [Development]

**Fun**

- A package of original fun commands made by Jojo.

**Modmail**

- A fluent easy-setup modmail cog produced by Jojo.

Support Server Changelog
------------------------

- Removed channels #poaching and #crystals from community category.
- Removed Titan and Otriux Cog Support Channels from Cog Support Category due to dormancy.
- Added Demaratus Announcement roles available to opt in and out of.
- Added a testing-beta channel for beta testing features.
- Added lavalink and hosting support channels.
- Removed inactive coding channels.
- Clarified Demaratus support rules.
- Changed rules.
- Other stuff that I can't remember.
- Added some roles, here and there. :D

Contact Support
---------------

You can receive support from the developers by joining our `Discord Development and Support Server <https://discord.gg/JmCFyq7>`_. Additionally, feel free to create issues or PRs on the `Kreusada's respository <https://github.com/KREUSADA/demaratus/>`_.

Plans for the future
--------------------

- Store user input and datas with config to develop currencies. No estimated ETA.
- Add more fun games for the community to enjoy.
- Bolster the UI of certain cogs such as moderation, to establish an improved authentic environment instead of standardred.
- Create games that involve currencies and storing user and user input data.

Recruitment
-----------

Ah, so you made it to the bottom of this document? In that case, we deem you worthy of a few roles we would like to offer as a thankyou to our users. If you would like to join the Demaratus Support Squad, we must first deem you knowledgable, but then we're happy to let you join the team. Additionally, we are looking for 1 new Staff member! If you would be interested, please let us know in the `Support Server <https://discord.gg/JmCFyq7>`_.





