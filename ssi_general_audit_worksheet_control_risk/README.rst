.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================================
General Audit Worksheet - Control Risk
======================================

This module provides worksheets for assessing and documenting **control risk**,
as required by ISA 315 / SA 315 (Identifying and Assessing the Risks of
Material Misstatement) and ISA 330 / SA 330 (The Auditor's Responses to
Assessed Risks).

Control risk is the risk that a material misstatement in an assertion could
occur and would not be prevented, or detected and corrected, by the entity's
internal control system on a timely basis.  The worksheets in this module
guide the auditor through a structured evaluation of:

1. **General Control Evaluation (d3d2719)** — Evaluates non-IT general
   controls (policies, procedures, organisational structure) using a
   configurable control set.  Each control is assessed against a set of
   indicators with customisable response options.
2. **IT Control Evaluation (f63f569)** — Evaluates IT general controls (ITGC)
   such as access management, change management, and IT operations, similarly
   structured as d3d2719 but with an IT-specific control set.
3. **Significant Account Internal Control (ba9b2f0)** — Evaluates key internal
   controls for a specific significant account type (e.g., Revenue, Receivables)
   and assesses overall control risk (Low / High) for that account.
4. **Business Cycle Internal Control (eabdaad)** — Evaluates key internal
   controls for a business cycle (e.g., Sales, Procurement) and assesses
   overall control risk (Low / High).
5. **Control Risk — Entity Level (b59b886)** — Consolidates the general and
   IT control evaluations at the entity level, identifying whether control
   deficiencies or significant deficiencies exist.
6. **Control Risk Summary (a58e29c)** — Aggregates the entity-level, cycle-level,
   and significant-account control-risk assessments onto one view to support the
   final control-risk conclusion for the engagement.

**Key features:**

- Configurable general-control and IT-control sets (``general_audit_general_control_set``,
  ``general_audit_it_control_set``) with indicator-level detail
- Auto-population of evaluation detail lines from the selected control set
- Risk conclusion (Low / High) per account type and business cycle
- Populated cross-links between worksheets (entity-level ↔ summary, etc.)
- Follows the standard worksheet workflow: Draft → Open → Confirm → Done

**Models (worksheets):**

- ``general_audit_ws_a58e29c``                      — Control Risk Summary
- ``general_audit_ws_b59b886``                      — Control Risk Entity Level
- ``general_audit_ws_b59b886.general_control``      — Entity-level general control evaluation line
- ``general_audit_ws_b59b886.it_control``           — Entity-level IT control evaluation line
- ``general_audit_ws_ba9b2f0``                      — Significant Account Internal Control
- ``general_audit_ws_ba9b2f0.detail``               — Control detail line per key control
- ``general_audit_ws_ba9b2f0.risk_identification``  — Risk identification line
- ``general_audit_ws_ba9b2f0.what_can_go_wrong``    — What-Can-Go-Wrong (WCGW) line
- ``general_audit_ws_d3d2719``                      — General Control Evaluation
- ``general_audit_ws_d3d2719.detail``               — Control detail line
- ``general_audit_ws_d3d2719.indicator``            — Indicator line
- ``general_audit_ws_eabdaad``                      — Business Cycle Internal Control
- ``general_audit_ws_eabdaad.detail``               — Control detail line per key control
- ``general_audit_ws_eabdaad.risk_identification``  — Risk identification line
- ``general_audit_ws_eabdaad.what_can_go_wrong``    — WCGW line
- ``general_audit_ws_f63f569``                      — IT Control Evaluation
- ``general_audit_ws_f63f569.detail``               — IT control detail line
- ``general_audit_ws_f63f569.indicator``            — IT indicator line

**Models (master data):**

- ``general_audit_assersion_type``             — Audit assertion types (completeness, accuracy, etc.)
- ``general_audit_control_activity``           — Control activity classification
- ``general_audit_general_control``            — General control item library
- ``general_audit_general_control_category``   — Category for general controls
- ``general_audit_general_control_set``        — Packaged set of general controls and indicators
- ``general_audit_general_control_indicator``  — Indicator for a general control
- ``general_audit_it_control``                 — IT control item library
- ``general_audit_it_control_category``        — Category for IT controls
- ``general_audit_it_control_set``             — Packaged set of IT controls and indicators
- ``general_audit_it_control_indicator``       — Indicator for an IT control
- ``general_audit_key_internal_control``       — Key internal control per business cycle
- ``general_audit_account_key_internal_control`` — Key internal control per significant account
- ``client_account_type`` (extension)          — Adds account-level key internal controls
- ``client_business_process`` (extension)      — Adds cycle-level key internal controls

**ISA / SA references:** ISA 315 / SA 315 — Identifying and Assessing the Risks
of Material Misstatement; ISA 330 / SA 330 — The Auditor's Responses to
Assessed Risks; ISA 265 / SA 265 — Communicating Deficiencies in Internal Control


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-general-audit
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *General Audit Worksheet - Control Risk*
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
