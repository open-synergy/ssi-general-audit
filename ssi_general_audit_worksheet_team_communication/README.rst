.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

============================================
General Audit Worksheet - Team Communication
============================================

This module provides worksheets for documenting engagement team communications
throughout a general audit engagement, in accordance with:

- **ISQC 1 / SA 220** — Quality Control for an Audit of Financial Statements
- **ISA 265 / SA 265** — Communicating Deficiencies in Internal Control
- **ISA 315 (Revised) / SA 315** — Identifying and Assessing Risks of Material Misstatement
- **ISA 240 / SA 240** — The Auditor's Responsibilities Relating to Fraud

Team communication is a required element at multiple stages of the audit. The
engagement team must discuss independence, competency, risk areas, and the
susceptibility of financial statements to material misstatement (including fraud).
This module captures those discussions as structured, checkable worksheets.

Worksheets Covered
==================

- **WS: Team Communication Pre-Engagement (437fc8f)** — Documents team discussions
  prior to and at the beginning of the engagement: acceptance, continuance, roles,
  independence, and preliminary planning consultations (ISQC 1 / SA 220).
- **WS: Team Communication Risk Assessment (b1f820c)** — Documents the engagement
  team's brainstorming on risks of material misstatement during the risk assessment
  phase, including fraud risks (ISA 315 / SA 315, ISA 240 / SA 240).

Key Features
============

- Checklist-based documentation with configurable master items per communication type
- Communication type classification: ``Engagement Team Understanding`` vs
  ``Consultation during the Engagement``
- Planning, execution, and reporting date tracking per communication session
- All worksheets follow the standard ``general_audit_worksheet_mixin`` architecture
  (delegated inheritance from ``general_audit_worksheet``)

Models
======

+---------------------------------------+-------------------------------------------------------+
| Model                                 | Description                                           |
+=======================================+=======================================================+
| ``general_audit_ws_437fc8f``          | WS: Team Communication Pre-Engagement                 |
+---------------------------------------+-------------------------------------------------------+
| ``general_audit_ws_437fc8f.checklist``| Pre-Engagement Communication — checklist value        |
+---------------------------------------+-------------------------------------------------------+
| ``general_audit_ws_437fc8f.item``     | Pre-Engagement Communication — master checklist item  |
+---------------------------------------+-------------------------------------------------------+
| ``general_audit_ws_b1f820c``          | WS: Team Communication Risk Assessment                |
+---------------------------------------+-------------------------------------------------------+
| ``general_audit_ws_b1f820c.checklist``| Risk Assessment Communication — checklist value       |
+---------------------------------------+-------------------------------------------------------+
| ``general_audit_ws_b1f820c.item``     | Risk Assessment Communication — master checklist item |
+---------------------------------------+-------------------------------------------------------+

Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-general-audit
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *General Audit Worksheet - Team Communication*
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
