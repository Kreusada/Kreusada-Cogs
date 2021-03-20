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