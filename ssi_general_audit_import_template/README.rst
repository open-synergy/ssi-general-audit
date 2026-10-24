.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============================
General Audit - Import Template
===============================

This module lets an administrator define the CSV template of each import in
General Audit as master data. A button on the template creates a server action
bound to the target model, so users download the template from the Action menu
of that model.

Key Features
============

- Master data of import templates, one or more per target model (for example
  one per client).
- Each template defines the file name, the delimiter, whether a header row is
  written, and its columns with a title and an example value.
- A button creates or removes the server action "Download Template: <name>".
- Three seeded templates match the existing import wizards: CoA And
  Mapping, Balance Amount, and Adjusting Journal. Their name, delimiter,
  example and columns follow the module version and are restored on every
  module update, so create a new template instead of editing a seeded one.
  A column added to a seeded template by hand is not removed by the update.
- Renaming a template renames its server action. A server action removed or
  unbound by an administrator is not created again by a module update, and
  an archived seeded template stays archived.

Models
======

+------------------------------------------+--------------------------------------+
| Model                                    | Description                          |
+==========================================+======================================+
| ``general_audit_import_template``        | Master: Import Template              |
+------------------------------------------+--------------------------------------+
| ``general_audit_import_template.line``   | Master: Import Template Column       |
+------------------------------------------+--------------------------------------+

Work Instruction
================

* `Create Import Template <docs/general_audit_import_template/index.html>`_
* `Create Server Action <docs/general_audit_import_template/index.html>`_

Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-general-audit
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *General Audit - Import Template*
6.  Install the module

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/open-synergy/ssi-general-audit/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.


Credits
=======

Contributors
------------

* Andhitia Rama <andhitia.r@gmail.com>
* Michael Viriyananda <viriyananda.michael@gmail.com>

Maintainer
----------

.. image:: https://simetri-sinergi.id/logo.png
   :alt: PT. Simetri Sinergi Indonesia
   :target: https://simetri-sinergi.id

This module is maintained by the PT. Simetri Sinergi Indonesia.
