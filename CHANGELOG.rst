============================
Changelog: Repository (Meta)
============================

This changelog includes all changes to the cog since 28/02/2021.
Versioning does not apply for meta unlike the changelogs for each specific cog.

----------
28/02/2021
----------

**Meta**

* Added repo-wide changelog
* Added changelog for AdvancedUptime
* Added changelog for BubbleWrap
* Added changelog for Codify
* Added changelog for Dehoister
* Added changelog for Edition
* Added changelog for NameGenerator
* Added changelog for PingInvoke
* Added changelog for RAM
* Added changelog for SendCards
* Added changelog for Staff
* Added changelog for TextManipulator
* Added changelog for TimesTables
* Added changelog for VoteChannel
* Added doclog labels

**Workflows**

* Update labelers to cohere with PRs into the BubbleWrap directory

**Cogs**

* ``Dehoister``: Fix issues relating to an undefined variable
* ``PingInvoke``: Update description key inside info.json

----------
01/03/2021
----------

**Cogs**

* Updated install messages for all cogs apart from ``edition``, to link to documentation
* ``PingOverride``: Improved UI of mapping kwargs
* ``PingOverride``: Change box lang for ping preview from python to yaml
* ``Dehoister``: Hoist scanning with more than 10 users now shows hoist count in the file

----------
01/03/2021
----------

**Cogs**

* ``Staff``: Change ``staff`` command bucket type from user to guild.
* ``Staff``: Improved embed UI
* ``Staff``: Added channel history for context
* ``Staff``: No longer send normal messages if not embed requested
* ``NameGenerator``: Sirnames don't have genders...
* ``SendCards``: Allow attachments in card sending
* ``SendCards``: Improve docstring detail 
* ``Staff``: Add asterix in optional arguments to allow proper reasons

----------
04/03/2021
----------

**Cogs**

* ``PingOverride``: Massive improvements to UI
* ``PingOverride``: New random choice feature
* ``PingOverride``: Enumerate output from preview
* ``PingOverride``: Better care over settings

----------
06/03/2021
----------

**Meta**

* ``Vinfo``: Added cog, with vast and major improvements
* ``Vinfo``: Fixed ``distutils.sysconfig`` attr error from import

----------
07/03/2021
----------

**Cogs**

* ``Vinfo``: Coverage for builtin modules and dependencies
* ``Vinfo``: Fixes for returning incorrect attribute
* ``Vinfo``: Check short attributes ``_version_``, ``version``

----------
13/03/2021
----------

**Cogs**

* ``Dehoister``: Provide dehoister immunity for bots
* ``Vinfo``: Add dependencies in aliases and usage
* ``Vinfo``: Use trigger typing when getting attributes

**Docs**

* ``Vinfo``: Added example images to user guide
* ``Index``: Add repository artwork

**Meta**

* Added repository artwork
* Enable PyLinter on push
* Enable Black on push

----------
14/03/2021
----------

**Cogs**

* ``AdvancedUptime``: Numerical data is now humanized

----------
20/03/2021
----------

**Cogs**

* ``Vinfo``: Fixes for sys, math, array and more, when they did not have ``__file__`` attributes.

**Meta**

* New cogs: ``ServerBlock``, ``Minifier``, ``Black``.