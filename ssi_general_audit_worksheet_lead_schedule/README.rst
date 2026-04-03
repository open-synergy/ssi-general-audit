.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=======================================
General Audit Worksheet - Lead Schedule
=======================================

This module provides worksheets for documenting the **lead schedules** and
**key audit procedures** as required by ISA 300 / SA 300 (Planning an Audit
of Financial Statements) and ISA 230 / SA 230 (Audit Documentation).

A lead schedule (also called a "top schedule" or "trial balance schedule") is
a working-paper document that lists the accounts under audit together with
their current balances, prior-year comparatives, audit adjustments, and
adjusted balances.  The worksheets in this module allow auditors to:

1. Maintain an aggregated, all-in-one lead schedule with every GL account
   included in the engagement and track adjustments at the account level.
2. Produce a per-account-type lead schedule showing account-level balances
   with supporting schedule cross-references.
3. Record and assign the **key audit procedures** that have been selected for
   each account type, together with the applicable assertion types and the
   engagement team member responsible for execution.

The module also registers the master-data models for **audit procedure
categories** and their individual **steps**, which form the library from which
the key-procedure worksheet is populated.

**Key features:**

- Automated loading/synchronisation of account lines from the General Audit
  detail list (action: *Load Accounts*)
- Balance-type toggle: *End Period* vs *Interim* balance
- Computed adjusted balance that applies debit/credit adjustments respecting
  the account's normal balance side
- Year-on-year percentage difference column
- Procedure steps linked to assertion types and assignable to team members

**Worksheets included:**

- ``general_audit_ws_b26d482``  — WS: All Accounts Lead Schedule (full trial balance)
- ``general_audit_ws_f9f3299``  — WS: Lead Schedule – per Account Type
- ``general_audit_ws_e51bb1c``  — WS: Key Audit Procedures per Account Type

**Master data models:**

- ``general_audit_audit_procedure_category`` — Audit procedure category master
- ``general_audit_audit_procedure``           — Audit procedure step master

**ISA / SA references:**

- ISA 230 / SA 230 — Audit Documentation
- ISA 300 / SA 300 — Planning an Audit of Financial Statements


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-general-audit
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *General Audit Worksheet - Lead Schedule*
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
