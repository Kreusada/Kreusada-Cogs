Ping Override
===============

--------
Overview
--------

PingOverride is a cog which allows you to override/overwrite the core's ping command with your own customisable response. This means that you can replace the "Pong." response, with something of your choosing. There are also additional options such as saying the author's name, and showing the bot latency. 

---------------------------
How do I download this cog?
---------------------------

Let's firstly add my repository if you haven't already:

* :code:`[p]repo add kreusada https://github.com/kreus7/kreusadacogs`

Next, let's download the cog from the repo:

* :code:`[p]cog install kreusada higherorlower`

Finally, you can see my end user data statement, cog requirements, and cog information by using:

* :code:`[p]cog info kreusada higherorlower`

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
  
--------
Support
--------

Feel free to visit my cog support channel in my `support server <https://discord.gg/JmCFyq7>`_, or head over to #support_othercogs in the 
`Red Cog Support Server <https://discord.gg/GET4DVk>`_, or you can file an `issue <https://github.com/kreus7/kreusadacogs/issues>`_ or a 
`pull request <https://github.com/kreus7/kreusadacogs/pulls>`_.
