.. _embedcreator:

============
EmbedCreator
============

This is the cog guide for the 'EmbedCreator' cog. This guide
contains the collection of commands which you can use in the cog.

Through this guide, ``[p]`` will always represent your prefix. Replace
``[p]`` with your own prefix when you use these commands in Discord.

.. note::

    This guide was last updated for version 1.1.0. Ensure
    that you are up to date by running ``[p]cog update embedcreator``.

    If there is something missing, or something that needs improving
    in this documentation, feel free to create an issue `here <https://github.com/Kreusada/Kreusada-Cogs/issues>`_.

    This documentation is auto-generated everytime this cog receives an update.

--------------
About this cog
--------------

Create embeds using buttons, modals and dropdowns!

--------
Commands
--------

Here are all the commands included in this cog (1):

* ``[p]embedcreate <options>``
    Create an embed.

   The command will send an interactive menu to construct an embed, unless otherwise specified by the **builder** option described further below.

   The following options are supported:
   - **title** - Embed title.
   - **description** - Embed description.
   - **colour/color** - A valid colour or hex code.
   - **url** - A valid URL for the embed's title hyperlink.
   - **image** - A valid URL for the embed's image.
   - **thumbnail** - A valid URL for the embed's thumbnail.
   - **author_name** - The name of the embed's author.
   - **author_url** - A valid URL for the author's hyperlink. 
   - **author_icon_url** - A valid URL for the author's icon image.
   - **footer_name** - Text for the footer.
   - **footer_icon_url** - A valid URL for the footer's icon image.
   - **builder** - Whether this help menu appears along with the constructor buttons. Defaults to true.
   - **source** - An existing message to use its embed. Can be a link or message ID.
   - **content** - The text sent outside of the message.

------------
Installation
------------

If you haven't added my repo before, lets add it first. We'll call it
"kreusada-cogs" here.

.. code-block:: ini

    [p]repo add kreusada-cogs https://github.com/Kreusada/Kreusada-Cogs

Now, we can install EmbedCreator.

.. code-block:: ini

    [p]cog install kreusada-cogs embedcreator

Once it's installed, it is not loaded by default. Load it by running the following
command:

.. code-block:: ini

    [p]load embedcreator

---------------
Further Support
---------------

For more support, head over to the `cog support server <https://discord.gg/GET4DVk>`_,
I have my own channel over there at #support_kreusada-cogs. Feel free to join my
`personal server <https://discord.gg/JmCFyq7>`_ whilst you're here.
