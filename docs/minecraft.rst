.. _minecraft:

=========
Minecraft
=========

.. attention:: This cog is not finished, but is listed for a sneak peak.

-------
Outline
-------

Minecraft *will* be a cog that allows you to ultimately build things inside of discord. 
With some easy-to-learn regex, you can build trees, buildings *with* windows, tnts, things
on fire with animated fire emojis, and more. You have control over what you decide to build, not me.

I hope to release other commands such as forgery, who is playing minecraft, and.. more? Maybe.

---------------------------
How do I download this cog?
---------------------------

Ahaha, I don't think so. This cog isn't quite ready yet and won't be findable on my repo.
However, feel free to add my repository in the meantime:

* :code:`[p]repo add kreusada https://github.com/kreus7/kreusadacogs`

-----
Usage
-----

* :code:`[p]build <construction_regex>`

For those who don't look at the regex patterns below, you will not understand how to build things in Discord.
Please consider taking a look. This command is one of multiple to come out.
Below, you will see all the regex types as of 18/01/21:

--------------
Regex Patterns
--------------

**Blocks**

:code:`t`: Denotes a TNT block.
:code:`d`: Denotes a dirt block.
:code:`s`: Denotes a sky block.
:code:`g`: Denotes a glass pane block.
:code:`f`: Denotes an 'on-fire' block. This block is animated.
:code:`w`: Denotes a birch wood block.
:code:`l`: Denotes a leaves block.
:code:`T`: Denotes a tree stalk block. 

**Utility**

:code:`b`: Denotes a completely empty block.
:code:`/`: Denotes a line break.

**Quantifiers**

:code:`<number>`: Represents the quantity of the attached block to spawn.
  - Syntax: :code:`[p]build <block_type><quantity>...`
  
.. note:: If no number is specified, it defaults to 1.

-------------
Example Usage
-------------

* :code:`[p]build w` - This will spawn a single wooden block. :code:`[p]build w1` also works in the same way.

* :code:`[p]build w5` - This will spawn 5 wooden blocks in a line.

* :code:`[p]build f/t` - This will spawn a fire block, with a TNT block underneath. The :code:`/` character allows us to line break.

* :code:`[p]build f5/t5` - This will spawn 5 fire blocks in a row, followed by 5 TNT blocks directly underneath.

* :code:`[p]build s6/s6/w6/w6/d6/d6` - This will spawn two rows of sky blocks, two rows of wooden blocks, and two rows of dirt blocks, each of which would be 6 in length.

* :code:`[p]build T/T/T/T` - This will spawn a vertical line of tree stalk blocks, 4 rows high.

* :code:`[p]build bTb/bTb/bTb/bTb` - This will spawn a vertical line of tree stalk blocks, 4 rows high. This will include blank blocks eitherside.

--------
Presets
--------

There are a few presets I have gathered to build certain objects.

**Syntax** - * :code:`[p]build s8/s8/s8/w4s2l2/wg2ws1l3/w4sl3/d8/d8`
**Output** - A small wooden building with a bush and some sky.




