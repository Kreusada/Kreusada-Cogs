.. _vinfo:

=====
Vinfo
=====

This is the cog guide for the vinfo cog. You will
find detailed docs about usage and commands.

Throughout this documentation, ``[p]`` is considered as your prefix.

------------
Installation
------------

Let's firstly add my repository if you haven't already:

* :code:`[p]repo add kreusada https://github.com/Kreusada/Kreusada-Cogs`

Next, let's download the cog from the repo:

* :code:`[p]cog install kreusada vinfo`

Finally, you can see my end user data statements, cog requirements, and other cog information by using:

* :code:`[p]cog info kreusada vinfo`

-----
Usage
-----

This cog will attempt to pull version attributes from modules
and third party cogs and provide you with their version.

.. _vinfo-commands:

--------
Commands
--------

Here's a list of all commands available for this cog.

.. _vinfo-command-vinfo:

^^^^^
vinfo
^^^^^

**Syntax**

.. code-block:: ini

    [p]vinfo

**Description**

Get versions of 3rd party cogs, and modules.

.. _vinfo-command-vinfo-cog:

"""""""""
vinfo cog
"""""""""

**Syntax**:

.. code-block:: ini

    [p]vinfo cog <cog>

**Description**

Get's the version of a third party cog. Some author's do not implement
version attributes in their cogs, meaning that this command may not be able to
return a version if it hasn't been defined in the cog's code.

**Arguments**

* ``<cog>``: The cog to get the version from.

.. warning:: The ``<cog>`` **must** be loaded, and provided in the correct case.

**Example Usage**

.. image:: /image_vinfo-cog.png
    :alt: vinfo cog

.. _vinfo-command-vinfo-mod:

"""""""""
vinfo mod
"""""""""

**Syntax**:

.. code-block:: ini

    [p]tt mod <module>

**Description**

Get a module's version information.

**Arguments**

* ``<module>``: The module to get the version from.

.. warning::

    The ``<module>`` **must** be installed, and provided in the correct case.
    There are a few modules such as `Levenshtein`, which start with capitals.

**Example Usage**

.. image:: /image_vinfo-mod.png
    :alt: vinfo mod

---------------
Receive Support
---------------

Feel free to ping me at the `Red Cog Support Server <https://discord.gg/GET4DVk>`_ in :code:`#support_kreusada-cogs`.
