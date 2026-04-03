.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

================================
General Audit Worksheet - Expert
================================

This module provides the worksheets for documenting the **evaluation of
experts** (both auditor-engaged and management-engaged) as required by
ISA 620 / SA 620 (Using the Work of an Auditor's Expert) and ISA 500 /
SA 500 (Audit Evidence).

When an expert's work is used during an audit, the auditor must evaluate
whether the expert has the competence, capabilities, and objectivity
necessary, and whether the scope and methods are adequate.  The worksheets
in this module cover:

1. **WS.040.1 — Auditor's Expert** — Documents the evaluation of an
   individual or organisation engaged directly by the auditor.  Evaluation
   factors are grouped by category (competence, capabilities, objectivity)
   and each factor is assessed with a free-text explanation.
2. **WS.040.2 — Management's Expert** — Documents the auditor's review of
   an expert engaged by management to produce information used as audit
   evidence.  Uses the same structured factor-based evaluation as WS.040.1.

**Key features:**

- Factor-based evaluation with configurable categories and factors
- Auto-populate detail lines from the master factor library
- Separate worksheets for auditor-engaged vs management-engaged experts
- Follows the standard worksheet workflow: Draft → Open → Confirm → Done

**Models:**

- ``general_audit_ws_bab9d32``          — WS.040.1 Auditor's Expert
- ``general_audit_ws_bab9d32.detail``   — Evaluation detail line (Auditor's Expert)
- ``general_audit_ws_bab9d32.factor``   — Evaluation factor master (Auditor's Expert)
- ``general_audit_ws_bab9d32.category`` — Factor category master (Auditor's Expert)
- ``general_audit_ws_cda3a68``          — WS.040.2 Management's Expert
- ``general_audit_ws_cda3a68.detail``   — Evaluation detail line (Management's Expert)
- ``general_audit_ws_cda3a68.factor``   — Evaluation factor master (Management's Expert)
- ``general_audit_ws_cda3a68.category`` — Factor category master (Management's Expert)
- ``mixin.expert``                      — Abstract mixin providing expert worksheet behaviour
- ``mixin.expert.detail``               — Abstract base for evaluation detail lines
- ``mixin.expert.factor``               — Abstract base for evaluation factor masters
- ``mixin.expert.category``             — Abstract base for factor categories

**ISA / SA references:** ISA 500 / SA 500 — Audit Evidence;
ISA 620 / SA 620 — Using the Work of an Auditor's Expert


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-general-audit
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *General Audit Worksheet - Expert*
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
