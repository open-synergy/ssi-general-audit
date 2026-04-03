.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============================================
General Audit Worksheet - Specific Procedures
=============================================

This module provides worksheets for specific audit procedures required during
the execution phase of a general audit engagement. It covers five critical audit
areas governed by ISA/SA standards:

- **ISA 501 / SA 501** — Commitments and Contingent Liabilities
- **ISA 540 / SA 540** — Auditing Accounting Estimates
- **ISA 550 / SA 550** — Related Parties
- **ISA 560 / SA 560** — Subsequent Events
- **ISA 570 / SA 570** — Going Concern (with Altman Z-Score computation)

Specific procedures are additional audit procedures designed to address
higher-risk areas or areas requiring special attention. This module allows
auditors to document their assessments for each of these audit areas, including
confirmation procedures, subsequent event classification, related party
identification, accounting estimation evaluation, and going concern analysis.

Worksheets Covered
==================

- **WS: Accounting Estimation (a8f4d88)** — Evaluates significant accounting
  estimates per account type in accordance with ISA 540, identifying the
  method used and any experts involved.
- **WS: Related Party Transaction (c40cfd9)** — Documents identified related
  parties, describes their transactions with the client, and tracks confirmation
  procedures performed in accordance with ISA 550.
- **WS: Subsequent Event (cb82c5f)** — Documents and classifies events after
  the balance sheet date (adjustment vs. non-adjustment events) and records
  auditor actions in accordance with ISA 560.
- **WS: Going Concern (fbf57ee)** — Assesses going concern indicators and
  performs Altman Z-Score computation to evaluate financial distress probability
  in accordance with ISA 570.
- **WS: Commitment and Contingent (ee819ae)** — Checklist-based evaluation
  of commitments and contingent liabilities in accordance with ISA 501.

Key Features
============

- Accounting estimate evaluation by account type with optional expert identification
- Related party identification table with confirmation procedure tracking
- Subsequent event classification (adjustment vs. non-adjustment) with occurrence status
- Going concern analysis using standard indicators plus Altman Z-Score computation
- Commitment & contingent checklist mapped to configurable master items
- All worksheets follow the standard ``general_audit_worksheet_mixin`` architecture
  (delegated inheritance from ``general_audit_worksheet``)

Models
======

+--------------------------------------------------------------+--------------------------------------------------+
| Model                                                        | Description                                      |
+==============================================================+==================================================+
| ``general_audit_ws_a8f4d88``                                 | WS: Accounting Estimation                        |
+--------------------------------------------------------------+--------------------------------------------------+
| ``general_audit_ws_a8f4d88.detail``                          | Accounting Estimation — detail per account type  |
+--------------------------------------------------------------+--------------------------------------------------+
| ``general_audit_ws_c40cfd9``                                 | WS: Related Party Transaction                    |
+--------------------------------------------------------------+--------------------------------------------------+
| ``general_audit_ws_c40cfd9.confirmation_procedure``          | Related Party — confirmation procedure line      |
+--------------------------------------------------------------+--------------------------------------------------+
| ``general_audit_ws_c40cfd9.related_party``                   | Related Party — identified related party entry   |
+--------------------------------------------------------------+--------------------------------------------------+
| ``general_audit_ws_cb82c5f``                                 | WS: Subsequent Event                             |
+--------------------------------------------------------------+--------------------------------------------------+
| ``general_audit_ws_cb82c5f.adjustment_detail``               | Subsequent Event — adjustment event line         |
+--------------------------------------------------------------+--------------------------------------------------+
| ``general_audit_ws_cb82c5f.non_adjustment_detail``           | Subsequent Event — non-adjustment event line     |
+--------------------------------------------------------------+--------------------------------------------------+
| ``general_audit_ws_fbf57ee``                                 | WS: Going Concern (Altman Z-Score)               |
+--------------------------------------------------------------+--------------------------------------------------+
| ``general_audit_ws_fbf57ee.analysis``                        | Going Concern — indicator analysis line          |
+--------------------------------------------------------------+--------------------------------------------------+
| ``general_audit_ws_fbf57ee.computation``                     | Going Concern — Z-Score computation line         |
+--------------------------------------------------------------+--------------------------------------------------+
| ``general_audit_ws_fbf57ee.confirmation_procedure``          | Going Concern — confirmation procedure line      |
+--------------------------------------------------------------+--------------------------------------------------+
| ``general_audit_ws_ee819ae``                                 | WS: Commitment and Contingent (checklist)        |
+--------------------------------------------------------------+--------------------------------------------------+
| ``general_audit_ws_ee819ae.checklist``                       | Commitment and Contingent — checklist line       |
+--------------------------------------------------------------+--------------------------------------------------+
| ``general_audit_ws_ee819ae.item``                            | Commitment and Contingent — checklist item       |
+--------------------------------------------------------------+--------------------------------------------------+
| ``general_audit_accounting_estimation_method``               | Master: Accounting Estimation Method             |
+--------------------------------------------------------------+--------------------------------------------------+
| ``general_audit_going_concern_z_score_coeficient_set``       | Master: Z-Score Coefficient Set                  |
+--------------------------------------------------------------+--------------------------------------------------+
| ``general_audit_going_concern_z_score_coeficient_set.item``  | Master: Z-Score Coefficient Set Item             |
+--------------------------------------------------------------+--------------------------------------------------+
| ``general_audit_related_party_confirmation_procedure``       | Master: Related Party Confirmation Procedure     |
+--------------------------------------------------------------+--------------------------------------------------+
| ``general_audit_going_concern_confirmation_procedure``       | Master: Going Concern Confirmation Procedure     |
+--------------------------------------------------------------+--------------------------------------------------+
| ``general_audit_subsequent_event``                           | Master: Subsequent Event Type                    |
+--------------------------------------------------------------+--------------------------------------------------+
| ``trial_balance_computation_item`` (ext.)                    | Extended: adds ``going_concern_ok`` flag         |
+--------------------------------------------------------------+--------------------------------------------------+

ISA/SA References
=================

- **ISA 501 / SA 501** — Audit Evidence: Specific Considerations for
  Selected Items (Commitments and Contingencies)
- **ISA 540 / SA 540** — Auditing Accounting Estimates, Including Fair Value
  Accounting Estimates, and Related Disclosures
- **ISA 550 / SA 550** — Related Parties
- **ISA 560 / SA 560** — Subsequent Events
- **ISA 570 / SA 570** — Going Concern


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-general-audit
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *General Audit Worksheet - Specific Procedures*
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
