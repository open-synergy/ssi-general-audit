.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=====================================================
General Audit Worksheet - Observation Audit Procedure
=====================================================

This module provides the worksheet for documenting **observation** audit
procedures, as required by ISA 500 / SA 500 (Audit Evidence) and ISA 315 /
SA 315 (Identifying and Assessing the Risks of Material Misstatement).

Observation consists of looking at a process or procedure being performed by
others — for example, watching entity personnel conduct a physical inventory
count or execute an internal control activity. Unlike inquiry (which relies on
the representations of knowledgeable persons), evidence obtained through
observation is restricted to the point in time at which the observation takes
place, so auditors typically supplement it with other corroborating procedures.

**Key features:**

- Links each observation session to a specific audit area via the Key Audit
  Procedures worksheet (Lead Schedule / WS-E51BB1C)
- Associates the observation with relevant financial statement assertions
  (e.g., Existence, Completeness, Rights & Obligations, Accuracy)
- Ties the observation to the relevant standard account type and business cycle
  (class of transaction)
- Captures background context and a primary concern identified before
  commencing the observation
- Supports a structured observation log
  (``general_audit_ws_d4d1ac0.observation``) so that each subject and its
  corresponding observation are individually documented
- Records an overall summary of findings after all observations are complete
- Follows the standard worksheet workflow: Draft → Open → Confirm → Done

**Models:**

- ``general_audit_ws_d4d1ac0`` — Main observation worksheet header
- ``general_audit_ws_d4d1ac0.observation`` — Individual observation lines
  (subject + observation detail) within an observation worksheet

**ISA / SA references:** ISA 500, SA 500 — Audit Evidence;
ISA 315, SA 315 — Identifying and Assessing the Risks of Material
Misstatement; ISA 330, SA 330 — The Auditor's Responses to Assessed Risks


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-general-audit
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *General Audit Worksheet - Observation Audit Procedure*
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
