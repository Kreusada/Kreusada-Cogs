.. _timestables:

===========
TimesTables
===========

This is the cog guide for the timestables cog. You will
find detailed docs about usage and commands.

Throughout this documentation, ``[p]`` is considered as your prefix.

------------
Installation
------------

Let's firstly add my repository if you haven't already:

* :code:`[p]repo add kreusada https://github.com/Kreusada/Kreusada-Cogs`

Next, let's download the cog from the repo:

* :code:`[p]cog install kreusada timestables`

Finally, you can see my end user data statements, cog requirements, and other cog information by using:

* :code:`[p]cog info kreusada timestables`

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

""""""""""
tt timeout
""""""""""

**Syntax**:

.. code-block:: ini

    [p]tt timeout <seconds>

**Description**

Sets how long you have to answer each question.

**Arguments**

* ``<seconds>``: The length of time per question in seconds.

---------------
Receive Support
---------------

Feel free to ping me at the `Red Cog Support Server <https://discord.gg/GET4DVk>`_ in :code:`#support_kreusada-cogs`.
