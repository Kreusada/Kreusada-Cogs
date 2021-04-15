.. _namegenerator:

=============
NameGenerator
=============

This is the cog guide for the namegenerator cog. You will
find detailed docs about usage and commands.

Throughout this documentation, ``[p]`` is considered as your prefix.

------------
Installation
------------

Let's firstly add my repository if you haven't already:

* :code:`[p]repo add kreusada https://github.com/kreusada/kreusadacogs`

Next, let's download the cog from the repo:

* :code:`[p]cog install kreusada namegenerator`

Finally, you can see my end user data statements, cog requirements, and other cog information by using:

* :code:`[p]cog info kreusada namegenerator`

------------
Requirements
------------

* ``names``

This cog requires the ``names`` module, so you will need to pip install it.

Now also uses ``thispersondoesnotexist``(https://pypi.org/project/thispersondoesnotexist/)

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

"""""""""
name picture
"""""""""

**Syntax**

.. code-block:: ini

    [p]name picture

**Description**

Gets a picture from https://thispersondoesnotexist.com/

**Arguments**
none

"""""""""
name profile
"""""""""

**Syntax**

.. code-block:: ini

    [p]name profile

**Description**

Gets a picture from https://thispersondoesnotexist.com/ as well as add a name to it
WARNING:AS THISPERSONDOESNOTEXIST IS RANDOM, THE GENDERS OF THE NAME AND PICURE MAY NOT MATCH!

**Arguments**
none


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
