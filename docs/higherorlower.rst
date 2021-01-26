.. _higherorlower:

===============
Higher Or Lower
===============

-------
Outline
-------

Higher or Lower is a standard card game which involves arbitrarily selecting a random card subsequent to your current card.
If you correctly guess that the next card is 'higher' or 'lower' than your current card, you advance to the next card.

In a standard game, there would be nine cards to arbitrarily advance through. This cog also has the default number of cards (9), 
but can be modified to your guild's liking via the :code:`[p]holset` command.

---------------------------
How do I download this cog?
---------------------------

Let's firstly add my repository if you haven't already:

* :code:`[p]repo add kreusada https://github.com/kreus7/kreusadacogs`

Next, let's download the cog from the repo:

* :code:`[p]cog install kreusada higherorlower`

Finally, you can see my end user data statement, cog requirements, and cog information by using:

* :code:`[p]cog info kreusada higherorlower`

-----
Usage
-----

* :code:`[p]hol`

:code:`hol`, as you may have guessed, stands for 'Higher Or Lower'! This command will allow you to start a game session with the guild's 
current features.

-----
Setup
-----

Setup is absolutely not required; if you want to keep things completely normal, you can start playing right away! 
However, customization is great, so there are a few settings that you can change to your GUILD's liking.
These settings are per guild to allow more customization for particular tastes in user interface and difficulty.
There are also settings per user which helps make your user's experience even greater!

.. code-block:: ini

  [p]holset image <bool>
  
This command allows you to set whether you would like the card image to be small, as a thumbnail, or large, as a full image.
Personally, I prefer having a smaller thumbnail, which is why I added both options. Images are great for desktop, whereas when you're 
on mobile, thumbnails are more appropriate for the smaller screen.

.. note:: This command is a setting personal to you, meaning that no one can change it except yourself.

This command is known as a boolean, meaning that you must specify either :code:`true` or :code:`false` after :code:`[p]holset image`.

.. code-block:: ini

  [p]holset total <int>
  
This command is locked to moderators or administrators, this setting will apply for everyone in your guild.
:code:`<int>` stands for integer. Here, you need to specify an integer which will determine the total number of 
cards your guild members have to work through to win.

.. attention:: 

  To be courteous to users, we've set a limit for this command.
  You cannot specify an integer less than 4, or greater than 20.
  
.. code-block:: ini

  [p]holset togglebank <bool>
  
This command is locked to moderators or administrators.
This command allows users to receive credits for each card they answer, or each round they complete. On installation, this setting's 
default is off. You must specify either :code:`true` or :code:`false`, if not, the boolean will default to :code:`false`.

Although you may have enabled the bank, the per card, and per round payouts default to zero. See the usage below to help configure these values.

.. warning::

  For these commands, **bank must be loaded.**
  
.. code-block:: ini

  [p]holset perpayout
  
This command is locked to moderators or administrators.
Sets the amount of credits that a user will receive per card that they correctly answer. On installation, this setting's default is 0.
The bank must be loaded through :code:`[p]load bank`, and it must be enabled via :code:`[p]holset togglebank true`, for transactions to take place.
You cannot specify a deposit above 1000.

.. code-block:: ini

  [p]holset roundpayout
  
This command is locked to moderators or administrators.
Sets the amount of credits that a user will receive per round that they complete. On installation, this setting's default is 0.
The bank must be loaded through :code:`[p]load bank`, and it must be enabled via :code:`[p]holset togglebank true`, for transactions to take place.
You cannot specify a deposit above 100000.

----------------
Additional Notes
----------------

And that's pretty much it! Thankyou for reading.

--------
Support
--------

Feel free to visit my cog support channel in my `support server <https://discord.gg/JmCFyq7>`_, or head over to #support_othercogs in the 
`Red Cog Support Server <https://discord.gg/GET4DVk>`_, or you can file an `issue <https://github.com/kreus7/kreusadacogs/issues>`_ or a 
`pull request <https://github.com/kreus7/kreusadacogs/pulls>`_.


**HigherOrLower** was released 11/01/2021.

`Home <https://kreusadacogs.readthedocs.io/en/latest/index.html>`_ | `Support Server <https://discord.gg/JmCFyq7>`_
