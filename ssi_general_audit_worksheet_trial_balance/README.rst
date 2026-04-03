.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=======================================
General Audit Worksheet - Trial Balance
=======================================

This module provides the trial balance worksheet used during the execution
phase of a general audit engagement. The trial balance is a fundamental audit
working paper that bridges the client's accounting records and the financial
statements under audit.

Relevant audit standards:

- **ISA 230 / SA 230** — Audit Documentation
- **ISA 300 / SA 300** — Planning an Audit of Financial Statements
- **ISA 500 / SA 500** — Audit Evidence

The trial balance worksheet ensures that auditors verify the completeness,
accuracy, and cast-correctness of the client's trial balance before conducting
substantive audit procedures on individual account areas.

Worksheets Covered
==================

- **WS: Trial Balance (a033cc6)** — Checklist-based verification that the
  client's trial balance is complete, agrees to the general ledger, and ties
  to the financial statements under audit. Supports tracking of audit
  adjustments and reclassification entries.

Key Features
============

- Configurable checklist items seeded from master data (verify footings,
  agree-to-GL, opening balance roll-forward, adjustment tracking)
- Checklist-based documentation ensuring all standard verification steps
  are completed before advancing to substantive procedures
- Follows the standard ``general_audit_worksheet_mixin`` architecture
  (delegated inheritance from ``general_audit_worksheet``)

Models
======

+---------------------------------------+----------------------------------------------------+
| Model                                 | Description                                        |
+=======================================+====================================================+
| ``general_audit_ws_a033cc6``          | WS: Trial Balance                                  |
+---------------------------------------+----------------------------------------------------+
| ``general_audit_ws_a033cc6.checklist``| Trial Balance — checklist value per item           |
+---------------------------------------+----------------------------------------------------+
| ``general_audit_ws_a033cc6.item``     | Trial Balance — master checklist item definition   |
+---------------------------------------+----------------------------------------------------+

Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-general-audit
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *General Audit Worksheet - Trial Balance*
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
