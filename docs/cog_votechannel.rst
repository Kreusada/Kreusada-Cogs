.. _votechannel:

===========
VoteChannel
===========

This is the cog guide for the votechannel cog. You will
find detailed docs about usage and commands.

Throughout this documentation, ``[p]`` is considered as your prefix.

------------
Installation
------------

Let's firstly add my repository if you haven't already:

* :code:`[p]repo add kreusada https://github.com/Kreusada/Kreusada-Cogs`

Next, let's download the cog from the repo:

* :code:`[p]cog install kreusada votechannel`

Finally, you can see my end user data statements, cog requirements, and other cog information by using:

* :code:`[p]cog info kreusada votechannel`

-----
Usage
-----

Designate multiple channels to have poll emojis reacted to each
message sent in them.

.. _votechannel-commands:

--------
Commands
--------

Here's a list of all commands available for this cog.

.. _votechannel-command-vote:

^^^^
vote
^^^^

**Syntax**

.. code-block:: ini

    [p]vote

**Description**

Commands with votechannel.

.. _votechannel-command-vote-channel:

""""""""""""
vote channel
""""""""""""

**Syntax**

.. code-block:: ini

    [p]vote channel

**Description**

Settings for channels.

.. _votechannel-command-vote-channel-add:

""""""""""""""""
vote channel add
""""""""""""""""

**Syntax**

.. code-block:: ini

    [p]vote channel add <channel>

**Description**

Add a channel to the votechannel list.

**Arguments**

* ``<channel>``: The Discord channel to receive poll reactions for each message sent inside it.

.. _votechannel-command-vote-channel-remove:

"""""""""""""""""""
vote channel remove
"""""""""""""""""""

**Syntax**

.. code-block:: ini

    [p]vote channel remove <channel>

**Description**

Remove a channel from the votechannel list.

**Arguments**

* ``<channel>``: The Discord channel to remove from the votechannel list.

.. _votechannel-command-vote-channel-list:

"""""""""""""""""
vote channel list
"""""""""""""""""

**Syntax**

.. code-block:: ini

    [p]vote channel list

**Description**

List the current voting channels.

.. _votechannel-command-vote-emoji:

""""""""""
vote emoji
""""""""""

**Syntax**

.. code-block:: ini

    [p]vote emoji

**Description**

Set and view the current emojis used for votechannel.

.. _votechannel-command-vote-emoji-down:

"""""""""""""""
vote emoji down
"""""""""""""""

**Syntax**

.. code-block:: ini

    [p]vote emoji down [emoji]

**Description**

Sets the downvote emoji for votechannel.

**Arguments**

* ``[emoji]``: The emoji to react with.

.. _votechannel-command-vote-emoji-down:

"""""""""""""
vote emoji up
"""""""""""""

**Syntax**

.. code-block:: ini

    [p]vote emoji up [emoji]

**Description**

Sets the upvote emoji for votechannel.

**Arguments**

* ``[emoji]``: The emoji to react with.

.. _votechannel-command-vote-emoji-presets:

""""""""""""""""""
vote emoji presets
""""""""""""""""""

**Syntax**

.. code-block:: ini

    [p]vote emoji presets

**Description**

Shows the current emojis used for votechannel.

.. _votechannel-command-vote-toggle:

"""""""""""
vote toggle
"""""""""""

**Syntax**

.. code-block:: ini

    [p]vote toggle

**Description**

Toggle votechannel.

---------------
Receive Support
---------------

Feel free to ping me at the `Red Cog Support Server <https://discord.gg/GET4DVk>`_ in :code:`#support_kreusada-cogs`.
