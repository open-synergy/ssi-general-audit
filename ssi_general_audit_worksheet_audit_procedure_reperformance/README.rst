.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=======================================================
General Audit Worksheet - Reperformance Audit Procedure
=======================================================

This module provides the worksheet for documenting **re-performance** audit
procedures, as required by ISA 500 / SA 500 (Audit Evidence) and ISA 330 /
SA 330 (The Auditor's Responses to Assessed Risks).

Re-performance involves the auditor's independent execution of procedures or
controls that were originally performed as part of the entity's internal
control system — for example, re-performing the ageing of accounts receivable,
re-reconciling a bank account, or independently re-executing an approval
workflow to confirm that the control operates as designed.

Unlike recalculation (which verifies mathematical accuracy only),
re-performance re-executes the **complete procedure end-to-end**. This makes
it especially effective as a **test of controls**: the auditor determines
whether the control would have detected or prevented a material misstatement.

**Key features:**

- Links each re-performance session to a specific audit area via the Key Audit
  Procedures worksheet (Lead Schedule / WS-E51BB1C)
- Associates the re-performance with relevant financial statement assertions
  (e.g., Completeness, Accuracy, Existence, Rights & Obligations)
- Ties the re-performance to the relevant standard account type for
  traceability in the overall audit file
- Follows the standard worksheet workflow: Draft → Open → Confirm → Done

**Models:**

- ``general_audit_ws_d1ecfb7`` — Main re-performance worksheet

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
5.  Search For *General Audit Worksheet - Reperformance Audit Procedure*
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
