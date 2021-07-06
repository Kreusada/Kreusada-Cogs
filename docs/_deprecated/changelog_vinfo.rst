.. _v-cl:

================
Vinfo: Changelog
================

This changelog includes all changes to the cog since 06/03/2021.

----------
06/03/2021
----------

* Fixed ``distutils.sysconfig`` attr error from import

----------
07/03/2021
----------

* Coverage for builtin modules and dependencies
* Fixes for returning incorrect attribute
* Check short attributes ``_version_``, ``version``

----------
13/03/2021
----------

* Add dependencies in aliases and usage
* Use trigger typing when getting attributes

----------
20/03/2021
----------

* Fixes for sys, math, array and more, when they did not have ``__file__`` attributes.

----------
29/03/2021
----------

* Various improvements to staticmethod and lambda sustainability.
* Support for lambda and unsupported instances of version attributes.
* Fix attribute errors for ``__spec__``s without ``origin`` kwargs.

----------
30/03/2021
----------

* Use ``importlib.machinery.ModuleSpec`` to check ``__spec__`` types.
* Use ``stdlib_list`` module to check for builtin modules.

----------
01/04/2021
----------

* Allow modules to be pip installed from a message predicate if it doesn't exist.

----------
04/04/2021
----------

* Use isinstance lambda instead of staticmethod for checking attr types in Vinfo.
