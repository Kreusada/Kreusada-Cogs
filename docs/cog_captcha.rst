.. _captcha:

=======
Captcha
=======

This is the cog guide for the 'Captcha' cog. This guide
contains the collection of commands which you can use in the cog.

Through this guide, ``[p]`` will always represent your prefix. Replace
``[p]`` with your own prefix when you use these commands in Discord.

.. note::

    This guide was last updated for version v1.0.2. Ensure
    that you are up to date by running ``[p]cog update captcha``.

    If there is something missing, or something that needs improving
    in this documentation, feel free to create an issue `here <https://github.com/Kreusada/Kreusada-Cogs/issues>`_.

    This documentation is auto-generated everytime this cog receives an update.

--------------
About this cog
--------------

A Captcha defensive system. to challenge the new users and protect yourself a bit more of
raids.

--------
Commands
--------

Here are all the commands included in this cog (15):

* ``[p]ownersetcaptcha``
 Set options for the Captcha cog.
* ``[p]ownersetcaptcha setlog <logging_level>``
 Set the logging level of the cog.
* ``[p]setcaptcha``
 Configure Captcha in your server.
* ``[p]setcaptcha allowedretries <number_of_retry>``
 Set the number of retries allowed before getting kicked.
* ``[p]setcaptcha autorole``
 Set the roles to give when passing the captcha.
* ``[p]setcaptcha autorole add [roles...]``
 Add a role to give.
* ``[p]setcaptcha autorole list``
 List all roles that will be given.
* ``[p]setcaptcha autorole remove [roles...]``
 Remove a role to give.
* ``[p]setcaptcha channel <text_channel_or_'dm'>``
 Set the channel where the user will be challenged.
* ``[p]setcaptcha enable <true_or_false>``
 Enable or disable Captcha security.
* ``[p]setcaptcha forgetme``
 Delete guild's data.
* ``[p]setcaptcha logschannel <text_channel_or_'none'>``
 Set a channel where events are registered.
* ``[p]setcaptcha temprole <temporary_role_or_'none'>``
 Give a temporary role when initilalizing the captcha challenge.
* ``[p]setcaptcha timeout <time_in_minutes>``
 Set the timeout before the bot kick the user if the user doesn't answer.
* ``[p]setcaptcha type <type_of_captcha>``
 Change the type of Captcha challenge.

------------
Installation
------------

If you haven't added my repo before, lets add it first. We'll call it
"kreusada-cogs" here.

.. code-block:: ini

    [p]repo add kreusada-cogs https://github.com/Kreusada/Kreusada-Cogs

Now, we can install Captcha.

.. code-block:: ini

    [p]cog install kreusada-cogs captcha

Once it's installed, it is not loaded by default. Load it by running the following
command:

.. code-block:: ini

    [p]load captcha

---------------
Further Support
---------------

For more support, head over to the `cog support server <https://discord.gg/GET4DVk>`_,
I have my own channel over there at #support_kreusada-cogs. Feel free to join my
`personal server <https://discord.gg/JmCFyq7>`_ whilst you're here.
