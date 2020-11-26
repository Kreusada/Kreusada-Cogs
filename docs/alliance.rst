.. _alliance::

========
Alliance
========

^^^^^^^^^^^^
How it works
^^^^^^^^^^^^

The ``alliance`` cog is used to alert movement for your fellow alliancemates, as well as additional tools which help your alliance move smoothly. This cog is dedicated to the mobile game Marvel Contest of Champions.

^^^^^^^^^^^^^^
Alliance Setup
^^^^^^^^^^^^^^

In `2.1.1 <https://kreusadacogs.readthedocs.io/en/latest/changelog_v2_1_1.html#v2-1-1>`_, we have changed how ``alertset`` works. Now, settings roles and channels is **not** compulsory.

**Setting your alliance role**

.. code-block:: none 

      dem alertset role <role>
      
This command configures an alliance role to be mentioned when alerts are sent out. Defaults to no role.

**Reset your alliance role**

.. code-block:: none

      dem alertset reset role

**Setting your alliance channel**

.. code-block:: none

      dem alertset channel <channel>

This command configures a channel for alliance alerts to be sent to. Defaults to the current channel of which the user sends the alert.

**Reset your alliance channel**

.. code-block:: none

      dem alertset reset channel
      
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Add your timezone to your nickname
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      dem timezone <timezone>
      
Adds your timezone to your nickname. For example, typing ``dem timezone +4`` would change my nickname to ``Kreusada [+4]``. If nothing is entered, your current timezone will be reset.

^^^^^^^^^^^^^^^^^^^^
Send alliance alerts
^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      dem alliancealert <alert>
      
.. note:: ``alliancealert`` has an alias of ``aa``. So you can instead use ``dem aa <alert`` for ease of access!

Your ``<alert>`` can vary from the six below:

**Alliance Quest Started**

.. code-block:: none

      dem alliancealert aqstart

.. note:: ``aqstart`` has an alias of ``aqs``. So you can instead use ``dem aa aqs`` for easy of access!

This command alerts your alliance for alliance quest.

**Alliance Quest Glory**

.. code-block:: none

      dem alliancealert aqglory

.. note:: ``aqglory`` has an alias of ``aqg``. So you can instead use ``dem aa aqg`` for easy of access!

This command alerts your alliance for alliance quest glory.

**Alliance War Placement**

.. code-block:: none

      dem alliancealert awplace

.. note:: ``awplace`` has an alias of ``awp``. So you can instead use ``dem aa awp`` for easy of access!

This command alerts your alliance for placing their defenders.

**Alliance War Attack**

.. code-block:: none

      dem alliancealert awattack

.. note:: ``awattack`` has an alias of ``awa``. So you can instead use ``dem aa awa`` for easy of access!

This command alerts your alliance for attacking their opponent.

**Alliance War Victory**

.. code-block:: none

      dem alliancealert awvictory

.. note:: ``awvictory`` has an alias of ``awv``. So you can instead use ``dem aa awv`` for easy of access!

This command alerts your alliance for when they win a war.

**Alliance War Defeat**

.. code-block:: none

      dem alliancealert awdefeat

.. note:: ``awdefeat`` has an alias of ``awd``. So you can instead use ``dem aa awd`` for easy of access!

This command alerts your alliance for when they lose a war.

^^^^^^^^^^^^^^^^^^^^^^^^^^^
Downloading for your redbot
^^^^^^^^^^^^^^^^^^^^^^^^^^^

My license emanates that my cogs are free for distribution and modification. However, claiming warranty or liability won't be accepted.

**Adding Kreusada's repository to your system**

- ``[p]repo add kreusada https://github.com/kreus7/kreusadacogs``

**Installing alliance into your cogs**

- ``[p]cog install kreusada alliance``

^^^^^^^^^^^^^^^^^^
Additional Support
^^^^^^^^^^^^^^^^^^

You can join our support server `here <https://discord.gg/JmCFyq7>`_.
This cog and cog guide was created by Kreusada for Demaratus.


      
