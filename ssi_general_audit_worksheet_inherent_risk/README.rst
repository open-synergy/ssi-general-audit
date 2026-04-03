.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================================================================
General Audit Worksheet - Inherent Risk
=================================================================

This module provides worksheets for the **inherent risk assessment** phase
of the audit engagement, as required by ISA 315 / SA 315 (Identifying and
Assessing the Risks of Material Misstatement through Understanding the
Entity and Its Environment), ISA 240 / SA 240 (Fraud), and ISA 570 / SA 570
(Going Concern).

Inherent risk assessment is a core component of the risk-based audit approach.
The auditor identifies and assesses the risks of material misstatement at both
the financial-statement level and the assertion level for each significant
account and disclosure area.  This module covers:

1. **WS.060.1 — Inherent Risk Assessment Checklist** — A configurable
   Yes / No / N-A checklist for evaluating inherent risk indicators at the
   financial-statement level.  Supplements the quantitative assessments in
   WS.060.2 and WS.060.3.
2. **WS.060.2 — Account Level Inherent Risk** — For each standard detail
   (account or disclosure area), the auditor selects inherent risk factors
   (with and without direct impact), assesses likelihood and magnitude, and
   derives an inherent risk level (low / medium / high).  Accounts assessed
   as *high likelihood + high impact + direct-impact factor* are flagged as
   **significant risks**.  Results are written back to the engagement's
   standard detail records for use by downstream worksheets.
3. **WS.060.3 — Financial Statement Level Inherent Risk** — Synthesises
   financial-statement level risks by consolidating review notes from
   upstream understanding-phase worksheets: Fraud Factor Analysis, Understanding
   of Preparation of Financial Statements, Going Concern Analysis, and
   Understanding of the Business Environment.

**Key features:**

- Master data for inherent risk factors with direct/indirect impact flags
- Automated computation of inherent risk level from likelihood × impact matrix
- Significant risk flag propagated back to ``general_audit.standard_detail``
- ``significant_risk_account_type_ids`` computed on ``general_audit`` for
  downstream consumption
- Predecessor worksheet checks ensure upstream worksheets are completed before
  this worksheet can be confirmed
- Follows the standard worksheet workflow: Draft → Open → Confirm → Done

**Models:**

- ``general_audit_ws_bfb6dae``           — WS.060.1 Inherent Risk Assessment Checklist
- ``general_audit_ws_bfb6dae.checklist`` — Checklist line
- ``general_audit_ws_bfb6dae.item``      — Checklist item master
- ``general_audit_ws_a418d89``           — WS.060.2 Account Level Inherent Risk
- ``general_audit_ws_a418d89.detail``    — Per-account risk assessment line
- ``general_audit_ws_c16abd7``           — WS.060.3 Financial Statement Level Inherent Risk
- ``general_audit_inherent_risk_factor`` — Inherent risk factor master data
- ``general_audit.standard_detail``      — Extended with inherent_risk and significant_risk fields
- ``general_audit``                      — Extended with significant_risk_account_type_ids computed field

**ISA / SA references:** ISA 240 / SA 240 — The Auditor's Responsibilities
Relating to Fraud; ISA 315 / SA 315 — Identifying and Assessing the Risks
of Material Misstatement through Understanding the Entity and Its Environment;
ISA 570 / SA 570 — Going Concern


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-general-audit
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *General Audit Worksheet - Understanding Entity and It's Environment*
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
