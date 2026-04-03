.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

================================================
General Audit Worksheet - External Communication
================================================

This module provides worksheets for documenting **external communications**
during the audit engagement, as required by ISA 260 / SA 260 (Communication
with Those Charged with Governance), ISA 265 / SA 265 (Communicating
Deficiencies in Internal Control), and ISA 610 / SA 610 (Using the Work
of Internal Auditors).

Effective communication with management, those charged with governance
(TCWG), and the internal audit function is a fundamental audit quality
requirement.  The worksheets in this module cover:

1. **WS.050.1 — External Communication Schedule** — Master schedule
   capturing the planned and actual dates of all communication activities
   with management, TCWG, and internal audit across planning, fieldwork,
   and reporting phases.
2. **WS.050.2 — Communication With Management** — Structured checklist
   of required communications with management, classified into:
   mutual understanding, audit-plan information, information to be
   obtained from management, and significant findings.
3. **WS.050.3 — Communication With TCWG** — Structured checklist of
   required communications with those charged with governance (board /
   audit committee), using the same four-category classification.
4. **WS.050.4 — Use of Internal Auditor's Work Results** — Evaluation
   checklist for deciding whether the internal audit function's work
   can be relied upon, covering objectivity, technical competence, and
   professional due care (ISA 610 / SA 610).

**Key features:**

- Date-tracking fields for each communication phase (planning, execution,
  reporting) with management, TCWG, and internal audit
- Communication-type classification for grouped reporting
- Configurable checklist item masters per worksheet
- Follows the standard worksheet workflow: Draft → Open → Confirm → Done

**Models:**

- ``general_audit_ws_ae48e68``           — WS.050.1 External Communication Schedule
- ``general_audit_ws_ae48e68.checklist`` — Checklist line (External Communication Schedule)
- ``general_audit_ws_ae48e68.item``      — Checklist item master
- ``general_audit_ws_b3ff42f``           — WS.050.2 Communication With Management
- ``general_audit_ws_b3ff42f.checklist`` — Checklist line (Communication With Management)
- ``general_audit_ws_b3ff42f.item``      — Checklist item master
- ``general_audit_ws_c94e287``           — WS.050.3 Communication With TCWG
- ``general_audit_ws_c94e287.checklist`` — Checklist line (Communication With TCWG)
- ``general_audit_ws_c94e287.item``      — Checklist item master
- ``general_audit_ws_d133f46``           — WS.050.4 Use of Internal Auditor's Work Results
- ``general_audit_ws_d133f46.checklist`` — Checklist line (Internal Auditor's Work)
- ``general_audit_ws_d133f46.item``      — Checklist item master

**ISA / SA references:** ISA 260 / SA 260 — Communication with Those
Charged with Governance; ISA 265 / SA 265 — Communicating Deficiencies
in Internal Control; ISA 610 / SA 610 — Using the Work of Internal Auditors


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-general-audit
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *General Audit Worksheet - External Communication*
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
