.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==============================
General Audit Worksheet - ROMM
==============================

This module provides the worksheets for documenting the **Risk of Material
Misstatement (ROMM) assessment** as required by ISA 315 / SA 315 (Identifying
and Assessing the Risks of Material Misstatement Through Understanding the
Entity and Its Environment).

The auditor is required to identify and assess the risks of material
misstatement at two levels:

* **Financial Statement Level** — Risks that relate pervasively to the
  financial statements as a whole and potentially affect many assertions.
* **Assertion Level** — Risks that relate to specific classes of transactions,
  account balances, or disclosures and that have a direct bearing on the
  sufficiency of audit procedures.

The worksheets in this module cover:

1. **WS: Financial Level ROMM (c165170)** — Documents the auditor's overall
   assessment of financial statement-level ROMM by aggregating identified
   risk factors from upstream worksheets: fraud factor analysis, entity-level
   control risk, understanding of financial statement preparation, prior audit
   findings, and business environment reviews.

2. **WS: Account Level ROMM (d66d87a)** — Captures ROMM assessment at the
   account / assertion level for every standard detail in the engagement.
   For each account the auditor records inherent risk, control risk, overall
   ROMM, and the planned responses (analytical procedures, tests of controls,
   tests of detail, interim procedures).

3. **WS: ROMM Checklist (de417a6)** — A structured Yes / No / N-A checklist
   confirming that all required risk assessment procedures have been performed
   and documented.

This module also extends the ``general_audit.standard_detail`` model with
assertion-level ROMM fields (P&D assertion types, inherent risk, planned
responses) used by the Account Level ROMM worksheet.

**Key features:**

- Auto-load account-level risk lines from the General Audit standard details
- Assertion types covering both Transaction-Level and Presentation &
  Disclosure (P&D) assertions tracked per account
- Planned response flags: Analytic Procedures, Tests of Controls (ToC),
  Tests of Detail (ToD), Interim procedures

**Models:**

- ``general_audit_ws_c165170``               — WS: Financial Level ROMM
- ``general_audit_ws_d66d87a``               — WS: Account Level ROMM
- ``general_audit_ws_d66d87a.detail``        — ROMM detail line per standard detail
- ``general_audit_ws_de417a6``               — WS: ROMM Checklist
- ``general_audit_ws_de417a6.checklist``     — Checklist answer line
- ``general_audit_ws_de417a6.item``          — Checklist item master
- ``general_audit.standard_detail``          — Extended with ROMM assessment fields

**ISA / SA references:** ISA 315 / SA 315 — Identifying and Assessing the
Risks of Material Misstatement Through Understanding the Entity and Its
Environment


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-general-audit
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *General Audit Worksheet - ROMM*
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
