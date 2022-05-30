.. _termino:

=======
Termino
=======

This is the cog guide for the 'Termino' cog. This guide
contains the collection of commands which you can use in the cog.

Through this guide, ``[p]`` will always represent your prefix. Replace
``[p]`` with your own prefix when you use these commands in Discord.

.. note::

    This guide was last updated for version 3.0.1. Ensure
    that you are up to date by running ``[p]cog update termino``.

    If there is something missing, or something that needs improving
    in this documentation, feel free to create an issue `here <https://github.com/Kreusada/Kreusada-Cogs/issues>`_.

    This documentation is auto-generated everytime this cog receives an update.

--------------
About this cog
--------------

Customize shutdown and restart messages, with the ability to add confirmation messages.

--------
Commands
--------

Here are all the commands included in this cog (10):

* ``[p]restart [force=False]``
 Attempts to restart [botname].
* ``[p]shutdown [force=False]``
 Shuts down the bot.
* ``[p]terminoset``
 Configure Termino messages.
* ``[p]terminoset restart``
 Set Termino's restart settings.
* ``[p]terminoset restart conf [message]``
 Set Termino's restart confirmation message.
* ``[p]terminoset restart message <message>``
 Set Termino's restart message.
* ``[p]terminoset settings``
 Shows the current settings for Termino.
* ``[p]terminoset shutdown``
 Set Termino's shutdown settings.
* ``[p]terminoset shutdown conf [message]``
 Set Termino's shutdown confirmation message.
* ``[p]terminoset shutdown message <message>``
 Set Termino's shutdown message.

------------
Installation
------------

If you haven't added my repo before, lets add it first. We'll call it
"kreusada-cogs" here.

.. code-block:: ini

    [p]repo add kreusada-cogs https://github.com/Kreusada/Kreusada-Cogs

Now, we can install Termino.

.. code-block:: ini

    [p]cog install kreusada-cogs termino

Once it's installed, it is not loaded by default. Load it by running the following
command:

.. code-block:: ini

    [p]load termino

---------------
Further Support
---------------

For more support, head over to the `cog support server <https://discord.gg/GET4DVk>`_,
I have my own channel over there at #support_kreusada-cogs. Feel free to join my
`personal server <https://discord.gg/JmCFyq7>`_ whilst you're here.
