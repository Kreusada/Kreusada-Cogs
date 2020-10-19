.. _tickets:

=====
Tickets
=====

This is a cog guide for the ``ticketer`` cog from Demaratus. The cog is very complex, this part of the documentation should cover all areas. 

.. warning:: This documentation is INCOMPLETE.

--------
Commands - Setup
--------

.. note:: You can learn how your users can create tickets further down this document.

-----
Setting Categories
-----

**Setting Categories: Open Tickets**

Use the following command to set the category for open tickets.

.. code-block:: none

  ,ticketer category open <category_id>

When a user creates a ticket using ``ticket create``, a ticket is created for them in this category. You must define this category for your ticketer setup.

**Setting Categories: Closed Tickets**

Use the following command to set the category for closed tickets.

.. code-block:: none

  ,ticketer category closed <category_id>

When a user closed a ticket using ``ticket close``, their open ticket is moved into this category. You must define this category for your ticketer setup.

-----
Ticket Management Channel
-----

Ticket Management channels are required for your ticketer setup.

**Ticket Management Channel Configuration**

.. code-block:: none

  ,ticketer channel <#channel>

When tickets are created, an embedded message is created in your ticket management channel, containing the name of the ticket, the reason, and the time.

-----
Ticket Name Type
-----



