.. _termino:

=======
Termino
=======

This is the cog guide for the termino cog. You will
find detailed docs about usage and commands.

Throughout this documentation, ``[p]`` is considered as your prefix.

------------
Installation
------------

Let's firstly add my repository if you haven't already:

* :code:`[p]repo add kreusada https://github.com/Kreusada/Kreusada-Cogs`

Next, let's download the cog from the repo:

* :code:`[p]cog install kreusada termino`

Finally, you can see my end user data statements, cog requirements, and other cog information by using:

* :code:`[p]cog info kreusada termino`

.. _termino-usage:

-----
Usage
-----

Customize bot shutdown and restart messages, with predicates, too.


.. note:: All commands within this cog are **locked** to bot owner.

.. _termino-commands:

--------
Commands
--------

.. _termino-command-restart:

^^^^^^^
restart
^^^^^^^

**Syntax**

.. code-block:: ini

    [p]restart [silently=False]

**Description**

Attempts to restart Red.

.. _termino-command-shutdown:

^^^^^^^^
shutdown
^^^^^^^^

**Syntax**

.. code-block:: ini

    [p]shutdown [silently=False]

**Description**

Shuts down Red.

.. _termino-command-terminoset:

^^^^^^^^^^
terminoset
^^^^^^^^^^

**Syntax**

.. code-block:: ini

    [p]terminoset

**Description**

Settings for the shutdown and restart commands.

.. _termino-command-terminoset-res:

""""""""""""""
terminoset res
""""""""""""""

**Syntax**

.. code-block:: ini

    [p]terminoset res <restart_message>

.. tip:: Alias: ``terminoset restart``

**Description**

Set and adjust the restart message.

**Arguments**

* ``<restart_message>``: The message to be sent on restarts.

.. _termino-command-terminoset-res-conf:

"""""""""""""""""""
terminoset res conf
"""""""""""""""""""

**Syntax**

.. code-block:: ini

    [p]terminoset res conf <true_or_false>

**Description**

Toggle whether restarts confirm before shutting down.

**Arguments**

* ``<true_or_false>``: Whether to toggle or not.

.. _termino-command-terminoset-res-conf:

"""""""""""""""""""""""""""""""
terminoset res restartedmessage
"""""""""""""""""""""""""""""""

**Syntax**

.. code-block:: ini

    [p]terminoset restartedmessage <restarted_message>

**Description**

Set the message to be sent after restarting.

The bot will attempt to send this message in the invoked channel.

**Arguments**

* ``<restarted_message>``: The message to send when the bot is back online.

.. _termino-command-terminoset-settings:

"""""""""""""""""""
terminoset settings
"""""""""""""""""""

**Syntax**

.. code-block:: ini

    [p]terminoset settings

**Description**

See the current settings for termino.

.. _termino-command-terminoset-shut:

"""""""""""""""
terminoset shut
"""""""""""""""

**Syntax**

.. code-block:: ini

    [p]terminoset shut <shutdown_message>

.. tip:: Alias: ``terminoset shutdown``

**Description**

Set and adjust the shutdown message.

**Arguments**

* ``<shutdown_message>``: The message to be sent on shutdowns.

.. _termino-command-terminoset-shut-conf:

""""""""""""""""""""
terminoset shut conf
""""""""""""""""""""

**Syntax**

.. code-block:: ini

    [p]terminoset shut conf <true_or_false>

**Description**

Toggle whether shutdowns confirm before shutting down.

**Arguments**

* ``<true_or_false>``: Whether to toggle or not.

---------------
Receive Support
---------------

Feel free to ping me at the `Red Cog Support Server <https://discord.gg/GET4DVk>`_ in :code:`#support_kreusada-cogs`.
