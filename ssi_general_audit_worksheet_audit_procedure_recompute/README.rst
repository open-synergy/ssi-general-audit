.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===================================================
General Audit Worksheet - Recompute Audit Procedure
===================================================

This module provides the worksheet for documenting **recalculation**
(recompute) audit procedures, as required by ISA 500 / SA 500
(Audit Evidence).

Recalculation consists of checking the mathematical accuracy of documents or
records — for example, independently verifying depreciation schedules, interest
accrual computations, payroll calculations, tax provisions, or totals in
financial schedules. Recalculation may be performed manually, with spreadsheet
software, or by re-running the client's own calculation model. Because it is
executed entirely by the auditor without reliance on client representations,
recalculation provides high-quality, reliable evidence for the **Accuracy** and
**Valuation** financial statement assertions.

**Key features:**

- Links each recalculation session to a specific audit area via the Key Audit
  Procedures worksheet (Lead Schedule / WS-E51BB1C)
- Associates the recalculation with relevant financial statement assertions
  (e.g., Accuracy, Valuation and Allocation)
- Ties the recalculation to the relevant standard account type and/or specific
  client account being audited
- Imports raw data from either a **General Ledger** (WS-D209914) or a
  **Subledger** (WS-B5E3D9F) worksheet, selected via the *Data Mode* field
- Provides configurable column mapping (Ref column, Original Amount column)
  and number-format settings (thousand/decimal separators)
- Allows the auditor to define a **recompute formula** using ``col_N``
  variables (e.g., ``col_3 + col_4 - col_5``) that reference columns from the
  raw data
- Automatically generates a comparison result (*Recompute Data*) containing
  Ref, Original Amount, Recompute Amount, Diff, and Result (Ok / Not Ok)
  columns
- Follows the standard worksheet workflow: Draft → Open → Confirm → Done

**Models:**

- ``general_audit_ws_c6c86fd`` — Main recalculation worksheet

**ISA / SA references:** ISA 500, SA 500 — Audit Evidence;
ISA 330, SA 330 — The Auditor's Responses to Assessed Risks;
ISA 520, SA 520 — Analytical Procedures


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-general-audit
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *General Audit Worksheet - Recompute Audit Procedure*
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
