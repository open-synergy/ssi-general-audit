.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============================================
General Audit Worksheet - Planning Memorandum
=============================================

This module provides the worksheets for documenting the **audit planning
memorandum** as required by ISA 300 / SA 300 (Planning an Audit of Financial
Statements).

Before fieldwork commences the auditor must prepare a planning memorandum
that summarises all key strategic and tactical decisions made during the
planning phase.  The planning memorandum serves as evidence that the audit was
properly planned and provides a reference for the audit team throughout the
engagement.

The worksheets in this module cover:

1. **WS: Audit Planning Memorandum — Checklist (a753ab9)** — A structured
   Yes / No / N-A checklist that systematically evaluates the five planning
   areas required by ISA 300: characteristics of the engagement, reporting
   objectives, important factors, significant changes and developments, and
   the nature / timing / extent of resources required.

2. **WS: Audit Planning Memorandum — Detail Summary (fbbe0f8)** — A
   consolidated narrative summary worksheet that aggregates key information
   from multiple upstream worksheets (business environment analysis, understanding
   of the entity, risk factors, materiality, and team roster) into a single,
   partner-reviewable document.  Dynamic labels in the form view are generated
   from the ``a753ab9`` item master.

**Key features:**

- Checklist items are categorised into planning areas and carry a
  ``related_field`` mapping that allows the detail summary to pull values
  automatically from linked upstream worksheets.
- The detail worksheet (fbbe0f8) aggregates: business-environment reviews,
  IT environment details, regulatory environment reviews, unannounced audit
  flags, materiality figures (overall / performance / tolerable misstatement),
  specific materiality mappings, team information, prior-year auditor details,
  and financial accounting standards.
- Both worksheets follow the standard workflow: Draft → Open → Confirm → Done.

**Models:**

- ``general_audit_ws_a753ab9``          — WS: Audit Planning Memorandum Checklist
- ``general_audit_ws_a753ab9.checklist`` — Checklist answer line
- ``general_audit_ws_a753ab9.item``      — Checklist item master
- ``general_audit_ws_fbbe0f8``          — WS: Audit Planning Memorandum Detail Summary

**ISA / SA references:** ISA 300 / SA 300 — Planning an Audit of Financial
Statements


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-general-audit
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *General Audit Worksheet - Planning Memorandum*
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
