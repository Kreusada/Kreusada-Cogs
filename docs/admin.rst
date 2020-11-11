.. _admin:

=====
Admin
=====

This is the cog guide for the admin cog. You will
find detailed docs about usage and commands.

.. _admin-usage:

-----
Usage
-----

This cog will provide tools for server admins.

It can add or remove a role to a member, edit one or make some available
for members so they can self-assign them as they wish.

.. _admin-commands:

--------
Commands
--------

Here's a list of all commands available for this cog.

.. _admin-command-selfrole:

^^^^^^^^
selfrole
^^^^^^^^

**Syntax**

.. code-block:: none

    ,selfrole

**Description**

Add or remove roles to yourself. Those roles must have been configured as user
settable by admins using the :ref:`selfroleset command
<admin-command-selfroleset>`.

.. _admin-command-selfrole-add:

""""""""""""
selfrole add
""""""""""""

**Syntax**

.. code-block:: none

    ,selfrole add <selfrole>

**Description**

Add a role to yourself. It must have been configured as user settable
by admins using the :ref:`selfroleset command <admin-command-selfroleset>`.

**Arguments**

* ``<selfrole>``: The role you want to attribute to yourself. |role-input|

.. _admin-command-selfrole-remove:

"""""""""""""""
selfrole remove
"""""""""""""""

**Syntax**

.. code-block:: none

    ,selfrole remove <selfrole>

**Description**

Remove a role from yourself. It must have been configured as user settable
by admins using the :ref:`selfroleset command <admin-command-selfroleset>`.

**Arguments**

* ``<selfrole>``: The role you want to remove from yourself. |role-input|


.. _admin-command-selfrole-list:

"""""""""""""
selfrole list
"""""""""""""

**Syntax**

.. code-block:: none

    ,selfrole list

**Description**

List all of the available roles you can assign to yourself.

.. _admin-command-selfroleset:

^^^^^^^^^^^
selfroleset
^^^^^^^^^^^

.. note:: |admin-lock| This is also usable by the members with the
    ``Manage roles`` permission.

**Syntax**

.. code-block:: none

    ,selfroleset

**Description**

Define the list of user settable roles. Those roles will be available to any
member using the :ref:`selfrole command <admin-command-selfrole>`.

.. _admin-command-selfroleset-add:

"""""""""""""""
selfroleset add
"""""""""""""""

**Syntax**

.. code-block:: none

    ,selfroleset add <role>

**Description**

Add a role to the list of selfroles.

.. warning:: Members will be able to assign themselves the role.
    Make sure it doesn't give extra perms or anything that can break
    your server's security.

**Arguments**

* ``<role>``: The role to add to the list. |role-input|

.. _admin-command-selfroleset-remove:

""""""""""""""""""
selfroleset remove
""""""""""""""""""

**Syntax**

.. code-block:: none

    ,selfroleset remove <role>

**Description**

Removes a role from the list of selfroles.

**Arguments**

* ``<role>``: The role to remove from the list. |role-input|

.. _admin-command-addrole:

^^^^^^^
addrole
^^^^^^^

.. note:: |admin-lock| This is also usable by the members with the ``Manage
    roles`` permission.

**Syntax**

.. code-block:: none

    ,addrole <rolename> [user]

**Description**

Adds a role to a member. If ``user`` is not given, it will be considered
as yourself, the command author.

**Arguments**

* ``<role>``: The role to add to the member. |role-input-quotes|

* ``[user]``: The member you want to add the role to. Defaults to the
  command author. |member-input|

.. _admin-command-removerole:

^^^^^^^^^^
removerole
^^^^^^^^^^

.. note:: |admin-lock| This is also usable by the members with the
    ``Manage roles`` permission.

**Syntax**

.. code-block:: none

    ,removerole <rolename> [user]

**Description**

Removes a role from a member. If ``user`` is not given, it will be considered
as yourself, the command author.

**Arguments**

* ``<role>``: The role to remove. |role-input-quotes|

* ``[user]``: The member to remove the role from. |member-input| Defaults
    to the command author.

.. _admin-command-editrole:

^^^^^^^^
editrole
^^^^^^^^

.. note:: |admin-lock|

**Syntax**

.. code-block:: none

    ,editrole

**Description**

Edits the settings of a role.

.. _admin-command-editrole-name:

"""""""""""""
editrole name
"""""""""""""

**Syntax**

.. code-block:: none

    ,editrole name <role> <name>

**Description**

Edits the name of a role.

**Arguments**

* ``<role>``: The role name to edit. |role-input-quotes|

* ``<name>``: The new role name. If it has spaces, you must use quotes.

.. _admin-command-editrole-color:

""""""""""""""
editrole color
""""""""""""""

**Syntax**

.. code-block:: none

    ,editrole color <role> <color>

**Description**

Edits the color of a role.

**Arguments**

* ``<role>``: The role name to edit. |role-input-quotes|

* ``<color>``: The new color to assign. |color-input|

**Examples**

* ``[p]editrole color "My role" #ff0000``

* ``[p]editrole color "My role" dark_blue``

.. _admin-command-announce:

.. note:: This cog guide was scripted by Kreusada and the Red Cog Creator Team.
