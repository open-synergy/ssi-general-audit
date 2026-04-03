.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============================================
General Audit Worksheet - Audit Working Plan
=============================================

This module provides the worksheet for documenting the **audit working plan**,
as required by ISA 300 / SA 300 (Planning an Audit of Financial Statements) and
ISA 220 / SA 220 (Quality Control for an Audit of Financial Statements).

The Audit Working Plan (WS-CBBBAF4) is prepared at the start of the engagement
planning phase to establish the overall strategic direction of the audit.  It
covers:

- **Overall audit timeline** — four key milestones are recorded: Pre-Engagement
  date, Risk Assessment date, Fieldwork date, and Pullout (wrap-up) date.
- **Man-hour budget** — total budget hours are allocated across the four audit
  phases (Pre-Engagement, Risk Assessment, Risk Response, and Reporting) using a
  configurable percentage template.  The budget status (Prepared / Not Prepared)
  tracks whether the budget has been finalised.
- **Team allocation** — each team member is assigned to the engagement with a
  role (e.g., Partner, Manager, Senior), and their planned hours per phase are
  recorded.
- **Team competency analysis** — the required competencies for the engagement
  are mapped against current team capabilities; any upgrade needs are identified
  and documented with supporting attachments.

**Key features:**

- Configurable man-hour allocation templates (``allocation_template``) with
  phase-percentage validation (must total 100%)
- Pre-defined total-hour master records (``allocation_total_hour``) for quick
  worksheet setup
- Team allocation lines automatically surfaced back on the general audit record
  via ``detail_team_allocation_ids``
- Competency-upgrade tracking linked to the skill matrix worksheet (b9d8a5c)
- Follows the standard worksheet workflow: Draft → Open → Confirm → Done

**Models:**

- ``general_audit_ws_cbbbaf4``                  — WS Audit Working Plan (main worksheet)
- ``general_audit_ws_cbbbaf4.team_allocation``  — Team member allocation per phase
- ``general_audit_ws_cbbbaf4.team_competency``  — Team competency analysis per member
- ``general_audit_competency_upgrade``          — Master: required competency upgrades
- ``allocation_template``                       — Master: man-hour allocation template
- ``allocation_total_hour``                     — Master: predefined total-hour values
- ``general_audit`` (extension)                 — Adds team-allocation aggregation
- ``res.company`` (extension)                   — Adds default allocation template

**ISA / SA references:** ISA 220 / SA 220 — Quality Control for an Audit;
ISA 300 / SA 300 — Planning an Audit of Financial Statements;
ISQM 1 — Quality Management for Firms that Perform Audits or Reviews


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
