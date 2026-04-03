.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

================================
General Audit Worksheet - Review
================================

This module provides the worksheets for documenting the **completion and
review** phase of the audit as required by ISA 700 / SA 700 series and
related standards.

During the completion phase the auditor reviews all audit work performed,
evaluates the sufficiency and appropriateness of evidence gathered, forms an
opinion on the financial statements, and reviews the draft auditor's report.

The worksheets in this module cover:

1. **WS: Audit Quality Review (bcc0d76)** — Aggregates a review summary for
   every main worksheet in the engagement.  For each worksheet it captures
   the state, review result, conclusion, and overall quality assessment.

2. **WS: Audit Evidence Evaluation Detail (cae598e)** — For each entry in
   the Audit Quality Review, the evaluator assesses whether audit evidence
   obtained is **sufficient and appropriate** (ISA 500 / SA 500) and whether
   any deficiencies or impacts on the audit opinion have been identified.

3. **WS: Audit Evidence Evaluation Checklist (dae9f3c)** — A structured
   Yes / No / N-A checklist that confirms overall audit evidence quality and
   completeness before the audit opinion is issued.

4. **WS: Financial Statement Disclosure Checklist (a025441)** — A detailed
   Yes / No / N-A checklist that verifies all required financial statement
   disclosures have been made in accordance with the applicable accounting
   standard (IFRS / PSAK / other).  Items are filtered by the financial
   accounting standard selected on the General Audit.

5. **WS: Financial Statement Disclosure Review (be62e79)** — A supplementary
   disclosure checklist organised by disclosure category (primary, additional,
   new) providing an additional level of review before sign-off.

6. **WS: Independent Auditor's Report Review (fc75636)** — A structured
   checklist to review the draft auditor's report for compliance with
   ISA 700 / SA 700.  Items are categorised by opinion type (unmodified,
   modified, emphasis of matter/other matter) and further grouped by report
   category.

**Key features:**

- Auto-populate quality review lines from all main worksheets (``action_populate``)
- Evidence evaluation linked 1-to-1 to quality review details
- Disclosure checklist filtered by the financial accounting standard
- Auditor's report checklist supporting all opinion types (unmodified and
  modified)

**Models:**

- ``general_audit_ws_bcc0d76``             — WS: Audit Quality Review
- ``general_audit_ws_bcc0d76.detail``      — Quality review detail line per worksheet
- ``general_audit_ws_cae598e``             — WS: Audit Evidence Evaluation Detail
- ``general_audit_ws_cae598e.detail``      — Evidence evaluation line
- ``general_audit_ws_dae9f3c``             — WS: Audit Evidence Evaluation Checklist
- ``general_audit_ws_dae9f3c.checklist``   — Checklist answer line
- ``general_audit_ws_dae9f3c.item``        — Checklist item master
- ``general_audit_ws_a025441``             — WS: Financial Statement Disclosure Checklist
- ``general_audit_ws_a025441.checklist``   — Checklist answer line
- ``general_audit_ws_a025441.item``        — Checklist item master
- ``general_audit_ws_be62e79``             — WS: Financial Statement Disclosure Review
- ``general_audit_ws_be62e79.checklist``   — Checklist answer line
- ``general_audit_ws_be62e79.item``        — Checklist item master
- ``general_audit_ws_fc75636``             — WS: Independent Auditor's Report Review
- ``general_audit_ws_fc75636.checklist``   — Checklist answer line
- ``general_audit_ws_fc75636.item``        — Checklist item master
- ``general_audit_ws_fc75636.category``    — Report section category master

**ISA / SA references:**

- ISA 500 / SA 500 — Audit Evidence
- ISA 700 / SA 700 — Forming an Opinion and Reporting on Financial Statements
- ISA 705 / SA 705 — Modifications to the Opinion in the Independent Auditor's Report
- ISA 706 / SA 706 — Emphasis of Matter Paragraphs and Other Matter Paragraphs
- ISA 720 / SA 720 — The Auditor's Responsibilities Relating to Other Information


Installation
Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-general-audit
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *General Audit Worksheet - Review*
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
