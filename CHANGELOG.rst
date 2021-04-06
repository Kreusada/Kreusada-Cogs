============================
Changelog: Repository (Meta)
============================

This changelog includes all changes to the cog since 28/02/2021.
Versioning does not apply for meta unlike the changelogs for each specific cog.

----------
28/02/2021
----------

* Added repo-wide changelogs.
* Added doclog labels.
* Update labelers to cohere with PRs into the BubbleWrap directory.
* Fix issues relating to an undefined variable in Dehoister.
* Update description key inside info.json in PingInvoke.

----------
01/03/2021
----------

* Updated install messages for all cogs apart from ``edition``, to link to documentation.
* Improved UI of mapping kwargs in PingOverride.
* Change box lang for ping preview from python to yaml in PingOverride.
* Hoist scanning with more than 10 users now shows hoist count in the file in Dehoister.

----------
01/03/2021
----------

* Change ``staff`` command bucket type from user to guild, with improved embed UI.
* Added channel history for context in Staff.
* No longer send normal messages if not embed requested, in Staff.
* Sirnames don't have genders in NameGenerator.
* Allow attachments in card sending, in SendCards.
* Add asterix in optional arguments to allow proper reasons in Staff.

----------
04/03/2021
----------

* Massive improvements to UI, new random choice feature, enumerate output from preview and better care over settings in PingOverride.

----------
06/03/2021
----------

* Initial revision of Vinfo, with vast and major improvements
* Fixed ``distutils.sysconfig`` attr error from import in Vinfo.

----------
07/03/2021
----------

* Coverage for builtin modules and dependencies in Vinfo.
* Fixes for returning incorrect attribute in Vinfo.
* Check short attributes ``_version_``, ``version``, in Vinfo.

----------
13/03/2021
----------

* Provide dehoister immunity for bots in Dehoister.
* Add dependencies in aliases and usage in Vinfo.
* Use trigger typing when getting attributes in Vinfo.
* Added example images to user guide in Vinfo.
* Add repository artwork to readme and docs.
* Enable PyLinter on push
* Enable Black on push

----------
14/03/2021
----------

* Humanize numerical data in AdvancedUptime

----------
20/03/2021
----------

* Fixes for sys, math, array and more, when they did not have ``__file__`` attributes in Vinfo.
* Initial revision of ``ServerBlock`` cog.
* Initial revision of ``Minifier`` cog.
* Initial revision of ``BlackFormatter`` cog.

----------
24/03/2021
----------


* Initial revision of ``AlphaNATO`` cog.
* Update usage to clarify that you can provide multiple letters in AlphaNATO.
* Fixed invalid URLS in info.json files (All Cogs).
* Remove unused imports from Black and Minifer cogs.
* Update labelers to include documentation for all cogs.
* Update CODEOWNERS to remove Edition and to add newer cogs.

----------
28/03/2021
----------

* Removed commands ``escape`` and ``remove`` from TextManipulator.
* Removed doclog labels from repository.

----------
29/03/2021
----------

* Various improvements to staticmethod and lambda sustainability in Vinfo.
* Support for lambda and unsupported instances of version attributes in Vinfo.
* Change `[p]name mash` concept to accept str, not discord.Member (NameGenerator)
* Fix attribute errors for ``__spec__``s without ``origin`` kwargs.

----------
30/03/2021
----------

* Use ``importlib.machinery.ModuleSpec`` to check ``__spec__`` types in Vinfo.
* Use ``stdlib_list`` module to check for builtin modules in Vinfo.

----------
01/04/2021
----------

* Allow modules to be pip installed from a message predicate if it doesn't exist in Vinfo.

----------
02/04/2021
----------

* Remove licenses from every cog, as I feel that it should not be displayed along with the code.
* Initial revision of ``RPSLS`` cog.

----------
04/04/2021
----------

* Initial revision of ``Quotes`` cog.
* Use isinstance lambda instead of staticmethod for checking attr types in Vinfo.
* Initial revision of ``ListRoles`` cog, and rename to ``RoleBoards`` to include more commands.

----------
05/04/2021
----------

* Fix labeler glob which would cause github checks to fail.
* Simplify lambdas by adding supporting staticmethods in RoleBoards.
* Fix attribute error with ``[p]staffset settings`` when a role doesn't exist, or is None.
* Greatly improved layout and coverage in repo-wide changelogs.
* Close aiohttp client session on cog unload in ``Quotes``.

----------
06/04/2021
----------

* Fix tabulate errors when a role is composed of chinese letters or emojis in RoleBoards.