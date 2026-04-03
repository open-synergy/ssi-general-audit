.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================================================
General Audit Worksheet - Preliminary Materiality
=================================================

This module provides the worksheets for documenting the **determination of
materiality** as required by ISA 320 / SA 320 (Materiality in Planning and
Performing an Audit).

Materiality is a fundamental concept in auditing.  During the planning phase
the auditor must establish:

* **Overall Materiality (OM)** — the threshold above which a misstatement is
  considered material to users of the financial statements.
* **Performance Materiality (PM)** — a lower threshold applied during
  fieldwork to reduce to an appropriately low level the probability that the
  aggregate of uncorrected and undetected misstatements exceeds OM.
* **Tolerable Misstatement (TM)** — the PM allocated to individual
  account balances or classes of transactions.

The worksheets in this module cover:

1. **WS: Materiality Computation (d9d2b44)** — Calculates OM, PM, and TM
   from a chosen base amount (e.g., total revenue, total assets, profit
   before tax) and user-defined percentages.  Supports both Extrapolation
   and End Period balance types.

2. **WS: Specific Materiality (6dcda0e)** — Maps each standard detail
   (account type) to either the overall or performance materiality benchmark
   and determines whether the account balance is *Material* or *Immaterial*.
   Allows the auditor to override and set a separate explicit specific
   materiality for individual accounts.

3. **WS: Preliminary Materiality Checklist (1d9338d)** — A structured
   Yes / No / N-A checklist covering the materiality determination process
   (materiality computation steps and material account mapping).

**Key features:**

- Formula-based computation of OM, PM, TM from a base figure and percentages.
- Automated determination of materiality classification (M / IM) per account.
- Override capability for specific materiality thresholds.
- Checklist items categorised by type: *Materiality Computation* and
  *Material Accounts Mapping*.

**Models:**

- ``general_audit_ws_d9d2b44``                          — WS: Materiality Computation
- ``general_audit_ws_6dcda0e``                          — WS: Specific Materiality
- ``general_audit_ws_6dcda0e_materiality_mapping``      — Materiality mapping line per account
- ``general_audit_ws_1d9338d``                          — WS: Preliminary Materiality Checklist
- ``general_audit_ws_1d9338d.checklist``                — Checklist answer line
- ``general_audit_ws_1d9338d.item``                     — Checklist item master

**ISA / SA references:** ISA 320 / SA 320 — Materiality in Planning and
Performing an Audit


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-general-audit
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *General Audit Worksheet - Preliminary Materiality*
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

Maintainer
----------

.. image:: https://simetri-sinergi.id/logo.png
   :alt: PT. Simetri Sinergi Indonesia
   :target: https://simetri-sinergi.id

This module is maintained by the PT. Simetri Sinergi Indonesia.
