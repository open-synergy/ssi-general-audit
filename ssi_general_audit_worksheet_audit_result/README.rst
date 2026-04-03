.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================================
General Audit Worksheet - Audit Result
======================================

This module provides the worksheets for documenting **audit results** at the
conclusion of fieldwork, as required by ISA 450 / SA 450 (Evaluation of
Misstatements), ISA 265 / SA 265 (Communicating Deficiencies in Internal
Control), ISA 700 / SA 700 (Forming an Opinion), and ISA 260 / SA 260
(Communication with Those Charged with Governance).

The Audit Result phase consolidates all open findings and control deficiencies
into a structured discussion and formulation process before the audit opinion
is signed.  The worksheets in this module cover:

1. **WR.110.1 — Findings That Influence Opinion** — The primary register for
   audit misstatements (factual, judgemental, or projected) accumulated during
   fieldwork.  Each finding is documented in the standard 5-C format (Condition,
   Criteria, Cause, Effect, Recommendation) and classified as *major* or
   *minor*.
2. **WR.110.2 — Control Deficiencies** — Documents identified internal
   control deficiencies.  Under ISA 265 / SA 265, significant deficiencies
   must be communicated in writing to those charged with governance.
3. **WR.110.3 — Audit Result Formulation** — Aggregates the findings from
   WR.110.1 and WR.110.2 onto a single engagement-partner view to support
   formulation of the audit opinion.
4. **WR.110.4 — Audit Result Discussion** — Records the formal audit results
   discussion with management, tracking whether each finding or deficiency has
   been *resolved* or *escalated* (e.g., to the Management Letter).

**Key features:**

- Captures findings and control deficiencies with the 5-C audit format
- Classifies severity (major / minor) for prioritisation and communication
- Automatically populates the discussion worksheet from upstream findings
- Tracks resolution status (resolved / escalated) per finding
- Follows the standard worksheet workflow: Draft → Open → Confirm → Done

**Models:**

- ``general_audit_ws_a0319a2``         — WR.110.1 Findings That Influence Opinion
- ``general_audit_ws_a0319a2.detail``  — Detail line for each finding
- ``general_audit_ws_d33420f``         — WR.110.2 Control Deficiencies
- ``general_audit_ws_d33420f.detail``  — Detail line for each deficiency
- ``general_audit_ws_ab19fd4``         — WR.110.3 Audit Result Formulation
- ``general_audit_ws_bc3e272``         — WR.110.4 Audit Result Discussion
- ``general_audit_ws_bc3e272.influence`` — Discussion line for findings
- ``general_audit_ws_bc3e272.control``   — Discussion line for deficiencies

**ISA / SA references:** ISA 260 / SA 260 — Communication with TCWG;
ISA 265 / SA 265 — Communicating Deficiencies in Internal Control;
ISA 450 / SA 450 — Evaluation of Misstatements Identified during the Audit;
ISA 700 / SA 700 — Forming an Opinion and Reporting on Financial Statements;
ISA 705 / SA 705 — Modifications to the Opinion in the Independent Auditor's Report


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-general-audit
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *General Audit Worksheet - Audit Result*
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
