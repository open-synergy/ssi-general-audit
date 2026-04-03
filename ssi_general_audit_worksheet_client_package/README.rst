.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===================================================
General Audit Worksheet - Client Assistance Package
===================================================

This module provides worksheets for collecting and organising **client-provided
data** (the Client Assistance Package, or CAP) required by the auditor to perform
fieldwork, as contemplated under ISA 500 / SA 500 (Audit Evidence) and
ISA 315 / SA 315 (Identifying and Assessing the Risks of Material Misstatement).

Auditors are required to obtain sufficient appropriate audit evidence.  A
structured client assistance package ensures that all necessary financial
schedules, supporting documents, and data files are received, organised, and
tied to the relevant audit areas before fieldwork begins.  This module covers:

1. **Client Assistance Package Checklist (abd82ed)** — A checklist of all
   documents, schedules, or data files the client must provide (current period
   or interim).  Items are marked complete once received and verified.
2. **Journal Entry Testing (e301171)** — A checklist-based worksheet for testing
   completeness and accuracy of journal entries, addressing the risk of management
   override of controls (ISA 240 / SA 240).
3. **Data Collection (f5a3cee)** — Tracks the receipt status of data per client
   account type.  Detail lines are auto-populated from the client's account
   mapping and include attachment evidence and a completion flag.
4. **Subledger (b5e3d9f)** — Imports CSV subledger data for a specific client
   account; parsed amounts are stored in separate amount lines for audit trail
   and analytical procedures.
5. **General Ledger (d209914)** — Imports CSV general-ledger transaction data
   for a specific client account, parsing debit/credit columns for lead-schedule
   reconciliation.

**Key features:**

- Checklist-driven worksheets (abd82ed, e301171) with completion tracking
- Flexible CSV import for subledger and general ledger data with configurable
  thousand/decimal separators and column mapping
- Attachment evidence per account-type detail line
- Position flag (current / interim) on the Client Assistance Package worksheet
- Follows the standard worksheet workflow: Draft → Open → Confirm → Done

**Models:**

- ``general_audit_ws_abd82ed``            — Client Assistance Package Checklist
- ``general_audit_ws_abd82ed.checklist``  — Checklist value line
- ``general_audit_ws_abd82ed.item``       — Checklist item master
- ``general_audit_ws_e301171``            — Journal Entry Testing Checklist
- ``general_audit_ws_e301171.checklist``  — Checklist value line
- ``general_audit_ws_e301171.item``       — Checklist item master
- ``general_audit_ws_f5a3cee``            — Data Collection tracker
- ``general_audit_ws_f5a3cee.detail``     — Detail line per account type
- ``general_audit_ws_b5e3d9f``            — Subledger data import
- ``general_audit_ws_b5e3d9f.amount``     — Parsed amount line per subledger column
- ``general_audit_ws_d209914``            — General Ledger data import

**ISA / SA references:** ISA 240 / SA 240 — Fraud in an Audit (journal entry
testing); ISA 500 / SA 500 — Audit Evidence; ISA 315 / SA 315 — Identifying
and Assessing the Risks of Material Misstatement


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-general-audit
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *General Audit Worksheet - Client Assistance Package*
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
