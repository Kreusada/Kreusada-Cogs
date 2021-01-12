.. _publishcogs:

================
Cog: PublishCogs
================

-------
Outline
-------

:code:`PublishCogs` is a cog which allows you to publish your new cogs to a specific channel in your guild! With a fully customizable output, you can set your new cogs to only display the author and cogname, or the author, cogname, description, pre-requirements, install guide and the current time on your embed's footer! Seems confusing, no? This guide should help you to get an understanding for this cog.

------------
Installation
------------

Make sure you have :code:`Downloader` loaded!

:code:`[p]load Downloader`

Let's add Kreusada's repository firstly:

:code:`[p]repo add kreusadacogs https://github.com/kreus7/kreusadacogs`

Now, you can add the :code:`PublishCogs` cog into your system.

:code:`[p]cog install kreusadacogs publishcogs`

-----
Usage
-----

- :code:`[p]publishcog`

Publishes cogs to a channel with a few questions to fill out first.

.. attention:: Setting your channel and cog creator role is a must before using these commands. Please contact an admin.

.. note:: Only Cog Creators will be able to use this command.

-----------
Setup Usage
-----------

- :code:`[p]publishcogset`

Configure settings for new cogs.

--------------
Setup: Channel
--------------

- :code:`[p]publishcogset channel <#channel>`

.. attention:: This setting is a **requirement** for this cog to work properly.

Set your channel for published cogs to be sent to.

-----------------
Setup: Footerdate
-----------------

- :code:`[p]publishcogset footerdate`

This is not a requirement. Running this command will bring you to a yes or no predicate which will determine your settings.

-----------------------
Setup: Cog Creator Role
-----------------------

- :code:`[p]publishcogset cogcreator`

.. attention:: This setting is a **requirement** for this cog to work properly.

Only those with the configured cog creator role will be able to use the :code:`[p]publishcog` command.

------------------
Setup: Description
------------------

- :code:`[p]publishcogset description`

.. tip:: This setting is not required, but is advised. Otherwise, the cog won't have a description! Unless you want it to remain anonymous, of course.

Sets the ability to add description for published cogs. Running this command will bring you to a yes or no predicate which will determine your settings.

----------------------
Setup: Prerequirements
----------------------

- :code:`[p]publishcogset prerequirements`

Sets the ability to add pre-requirements for published cogs. Running this command will bring you to a yes or no predicate which will determine your settings.

--------------------
Setup: Install Guide
--------------------

- :code:`[p]publishcogset installguide`

.. tip:: This setting is not required, but is advised. Otherwise, the cog won't have an install guide.

Sets the ability to add an install guide for published cogs. Running this command will bring you to a yes or no predicate which will determine your settings.

--------------
Setup: Set All
--------------

- :code:`[p]publishcogset setall`

This command will toggle all toggleable commands on, or off! Running this command will bring you to a yes or no predicate which will determine your settings.






