.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=========================================
General Audit - Import Template Worksheet
=========================================

This module seeds import templates for the worksheets whose raw data is pasted
by the user as CSV: Subledger, General Ledger, Population, and Financial
Statement Disclosure. It is separate from the core template module so the core
does not force the worksheet modules to be installed.

Key Features
============

- Four seeded templates. Their name, delimiter, example and columns follow
  the module version and are restored on every module update, so create a new
  template instead of editing a seeded one. A column added to a seeded
  template by hand is not removed by the update. A server action removed or
  unbound by an administrator is not created again by a module update, and an
  archived seeded template stays archived.
- Financial Statement Disclosure - Detail: columns Item, Standard, Note, and Status.
- Population: illustrative columns only (ID, Date, Reference, Amount).
- Subledger: per-item balance list with columns No, Name, Reference, Date,
  Due Date, and Amount.
- General Ledger: columns Date, Reference, Account Code, Account Name,
  Description, Debit, and Credit.
- The columns are examples, not a mandatory format. The amount columns are
  chosen by the user per worksheet, so adjust per client.
- No server action is created automatically; press *Create Server Action* on
  the template to offer the download in the Action menu.

Models
======

This module adds no model. It seeds data of ``general_audit_import_template``.

Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-general-audit
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *General Audit - Import Template Worksheet*
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
