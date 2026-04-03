.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===================================================================
General Audit Worksheet - Final Materiality & Analytical Procedures
===================================================================

This module provides worksheets for the **final materiality reassessment**
and **final analytical procedures** performed at the conclusion of audit
fieldwork, as required by ISA 320 / SA 320 (Materiality) and ISA 520 /
SA 520 (Analytical Procedures).

At the end of fieldwork the auditor is required to:

1. Reassess the materiality levels used during planning against the final
   audited financial amounts.
2. Apply overall analytical procedures to form a general conclusion about
   whether the financial statements as a whole are consistent with the
   auditor's understanding of the entity.

The worksheets in this module cover:

1. **WS.080.1 — Final Materiality** — Consolidates overall materiality
   (OM), performance materiality (PM), and tolerable misstatement (TM) for
   three stages: planning, end-period (unaudited), and audited.  Computes
   and documents the variances between stages to support the auditor's
   professional judgement on whether the planning materiality remains
   appropriate.
2. **WS.080.2 — Final Analytical Procedures Checklist** — Checklist
   confirming completion of all required analytical procedures, classified
   by analysis type (vertical/horizontal or ratio).
3. **WS.080.3 — Final Analytical Procedures — Vertical and Horizontal
   Analysis** — Quantitative comparison of all standard-detail line items
   across previous, end-period, and audited trial balances using common-
   size (vertical) and trend (horizontal) analysis.  Loaded from the
   corresponding Preliminary Analytic Procedure worksheet.
4. **WS.080.4 — Final Analytical Procedures — Ratio Analysis** — Computes
   financial ratios (liquidity, solvency, profitability, etc.) for the
   previous, end-period, and audited periods and compares them against
   industry averages.  Loaded from the corresponding Preliminary Ratio
   Analysis worksheet.

**Key features:**

- Three-way materiality comparison (planning vs unaudited vs audited)
- Automated variance computations for OM, PM, and TM
- Action to load analysis lines from the preliminary analytic procedure
- Configurable financial ratio library with Python-formula evaluation
- Follows the standard worksheet workflow: Draft → Open → Confirm → Done

**Models:**

- ``general_audit_ws_bb33b94`` — WS.080.1 Final Materiality
- ``general_audit_ws_c2375d8`` — WS.080.2 Final Analytical Procedures Checklist
- ``general_audit_ws_c2375d8.checklist`` — Checklist line
- ``general_audit_ws_c2375d8.item``      — Checklist item master
- ``general_audit_ws_e1f2d98`` — WS.080.3 Final Analytic Procedures — VH Analysis
- ``general_audit_ws_e1f2d98.vertical_horizontal_analysis`` — VH analysis detail line
- ``general_audit_ws_f3a78de`` — WS.080.4 Final Analytic Procedures — Ratio Analysis
- ``general_audit_ws_f3a78de.ratio``     — Ratio analysis detail line

**ISA / SA references:** ISA 320 / SA 320 — Materiality in Planning and
Performing an Audit; ISA 450 / SA 450 — Evaluation of Misstatements;
ISA 520 / SA 520 — Analytical Procedures


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-general-audit
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *General Audit Worksheet - Final Materiality & Analytical Procedures*
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
