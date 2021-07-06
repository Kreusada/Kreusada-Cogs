.. _quotes:

======
Quotes
======

This is the cog guide for the quotes cog. You will
find detailed docs about usage and commands.

Throughout this documentation, ``[p]`` is considered as your prefix.

------------
Installation
------------

Let's firstly add my repository if you haven't already:

* :code:`[p]repo add kreusada https://github.com/Kreusada/Kreusada-Cogs`

Next, let's download the cog from the repo:

* :code:`[p]cog install kreusada quotes`

Finally, you can see my end user data statements, cog requirements, and other cog information by using:

* :code:`[p]cog info kreusada quotes`

.. _quotes-usage:

-----
Usage
-----

Get a random quote.


.. _quotes-commands:

--------
Commands
--------

.. _quotes-command-quote:

^^^^^
quote
^^^^^

**Syntax**

.. code-block:: ini

    [p]quote

**Description**

Get a random quote.

.. tip::

    We can use bobloy's `FIFO <https://github.com/bobloy/Fox-V3/tree/master/fifo>`_
    cog, with this cog, to run QOTD (Quote of the day).

    **Steps**

    1. ``[p]fifo add qotd quote``
    2. ``[p]fifo addtrigger cron qotd 0 0 * * *``
    3. ``[p]fifo set qotd <feed_channel>``

    Your feed channel is whatever channel you'd like QOTD to be posted in.

---------------
Receive Support
---------------

Feel free to ping me at the `Red Cog Support Server <https://discord.gg/GET4DVk>`_ in :code:`#support_kreusada-cogs`.
