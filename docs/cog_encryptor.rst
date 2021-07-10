.. _encryptor:

=========
Encryptor
=========

This is the cog guide for the encryptor cog. You will
find detailed docs about usage and commands.

Throughout this documentation, ``[p]`` is considered as your prefix.

------------
Installation
------------

Let's firstly add my repository if you haven't already:

* :code:`[p]repo add kreusada https://github.com/Kreusada/Kreusada-Cogs`

Next, let's download the cog from the repo:

* :code:`[p]cog install kreusada encryptor`

Finally, you can see my end user data statements, cog requirements, and other cog information by using:

* :code:`[p]cog info kreusada encryptor`

.. _encryptor-usage:

-----
Usage
-----

Create, save, and validify passwords.


.. _encryptor-commands:

--------
Commands
--------

.. _encryptor-command-password:

^^^^^^^^
password
^^^^^^^^

**Syntax**

.. code-block:: ini

    [p]password

**Description**

Create, save, and validify passwords.

.. _encryptor-command-password-generate:

"""""""""""""""""
password generate
"""""""""""""""""

**Syntax**

.. code-block:: ini

    [p]password generate

**Description**

Generate passwords.

.. _encryptor-command-password-generate-complex:

"""""""""""""""""""""""""
password generate complex
"""""""""""""""""""""""""

**Syntax**

.. code-block:: ini

    [p]password generate complex

**Description**

Generate a complex password.

.. _encryptor-command-password-generate-strong:

""""""""""""""""""""""""
password generate strong
""""""""""""""""""""""""

**Syntax**

.. code-block:: ini

    [p]password generate strong [delimeter]

**Description**

Generate a strong password.

**Arguments**

* ``<delimeter>``: The character used to seperate each random word. Defaults to "-"

.. _encryptor-command-password-strength:

"""""""""""""""""
password strength
"""""""""""""""""

**Syntax**

.. code-block:: ini

    [p]password strength <password>

**Description**

Validate a passwords strength.

**Arguments**

* ``<password>``: The password to get a strength rating for.

---------------
Receive Support
---------------

Feel free to ping me at the `Red Cog Support Server <https://discord.gg/GET4DVk>`_ in :code:`#support_kreusada-cogs`.
