.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

========================================================
General Audit Worksheet - Preliminary Analytic Procedure
========================================================

This module provides the worksheets for documenting **preliminary analytical
procedures** as required by ISA 315 / SA 315 (Identifying and Assessing the
Risks of Material Misstatement) and ISA 520 / SA 520 (Analytical Procedures).

Preliminary analytical procedures are performed during the planning phase to
obtain an understanding of the client's business and to identify unusual
fluctuations or relationships that may indicate material misstatement risks.
The auditor uses these procedures to direct attention to high-risk areas and
to determine the nature, timing, and extent of other audit procedures.

The worksheets in this module cover:

1. **WS: Vertical and Horizontal Analysis (b32655a)** — Computes period-over-
   period percentage changes (horizontal analysis) and common-size proportions
   (vertical analysis) for each standard detail line.  Supports both
   Extrapolation (forecasted) and End Period balance types.

2. **WS: Ratio Analysis (d4289e4)** — Computes standard financial ratios
   (liquidity, activity, profitability, solvency) for the current period using
   client financial ratio definitions.  Supports End Period and Extrapolation
   balance types.  Each ratio is evaluated against its prior-period audited
   figure and the industry average.

3. **WS: Preliminary Analytic Procedure — Summary (c8740d4)** — The main
   worksheet for this phase; includes a structured checklist that the auditor
   completes to document results and an open narrative conclusion section
   organised by category.

**Key features:**

- Auto-load analysis lines from the General Audit standard detail list
- Balance type selection: Extrapolation vs. End Period
- Ratio computation via configurable Python formulas in the ``client_financial_ratio``
  master
- Conclusion narratives grouped by ``analytic_procedure_conclusion_category``

**Models:**

- ``general_audit_ws_b32655a``               — WS: Vertical and Horizontal Analysis
- ``general_audit_ws_b32655a.vertical_horizontal_analysis`` — Analysis detail line
- ``general_audit_ws_d4289e4``               — WS: Ratio Analysis
- ``general_audit_ws_d4289e4.ratio``         — Ratio computation line
- ``general_audit_ws_c8740d4``               — WS: Preliminary Analytic Procedure Summary
- ``general_audit_ws_c8740d4.checklist``     — Checklist answer line
- ``general_audit_ws_c8740d4.item``          — Checklist item master
- ``general_audit_ws_c8740d4.analytic_procedure_conclusion`` — Conclusion line
- ``analytic_procedure_conclusion_category`` — Conclusion category master

**ISA / SA references:**

- ISA 315 / SA 315 — Identifying and Assessing the Risks of Material Misstatement
- ISA 520 / SA 520 — Analytical Procedures


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-general-audit
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *General Audit Worksheet - Preliminary Analytic Procedure*
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
