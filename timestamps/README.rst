.. _timestamps:

==========
TimeStamps
==========

This is the cog guide for the 'TimeStamps' cog. This guide
contains the collection of commands which you can use in the cog.

Through this guide, ``[p]`` will always represent your prefix. Replace
``[p]`` with your own prefix when you use these commands in Discord.

.. note::

    This guide was last updated for version 1.2.0. Ensure
    that you are up to date by running ``[p]cog update timestamps``.

    If there is something missing, or something that needs improving
    in this documentation, feel free to create an issue `here <https://github.com/Kreusada/Kreusada-Cogs/issues>`_.

    This documentation is auto-generated everytime this cog receives an update.

--------------
About this cog
--------------

Retrieve timestamps for certain dates.

--------
Commands
--------

Here are all the commands included in this cog (1):

+------------------+-------------------------------------------------------------------+
| Command          | Help                                                              |
+==================+===================================================================+
| ``[p]timestamp`` | Produce a Discord timestamp.                                      |
|                  |                                                                   |
|                  | Timestamps are a feature added to Discord in the summer of 2021,  |
|                  | which allows you to send timestamps will which update accordingly |
|                  | with any user's date time settings.                               |
|                  |                                                                   |
|                  | **Example Usage**                                                 |
|                  |                                                                   |
|                  | - `[p]timestamp 1st of october 2021`                              |
|                  | - `[p]timestamp 20 hours ago raw:true`                            |
|                  | - `[p]timestamp in 50 minutes`                                    |
|                  | - `[p]timestamp 01/10/2021 format:f`                              |
|                  | - `[p]timestamp now raw:true format:R`                            |
+------------------+-------------------------------------------------------------------+

------------
Installation
------------

If you haven't added my repo before, lets add it first. We'll call it
"kreusada-cogs" here.

.. code-block:: ini

    [p]repo add kreusada-cogs https://github.com/Kreusada/Kreusada-Cogs

Now, we can install TimeStamps.

.. code-block:: ini

    [p]cog install kreusada-cogs timestamps

Once it's installed, it is not loaded by default. Load it by running the following
command:

.. code-block:: ini

    [p]load timestamps

---------------
Further Support
---------------

For more support, head over to the `cog support server <https://discord.gg/GET4DVk>`_,
I have my own channel over there at #support_kreusada-cogs. Feel free to join my
`personal server <https://discord.gg/JmCFyq7>`_ whilst you're here.
