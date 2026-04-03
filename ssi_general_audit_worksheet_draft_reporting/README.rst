.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=========================================
General Audit Worksheet - Draft Reporting
=========================================

This module provides the worksheets that govern the **draft reporting** phase
of the general audit, covering the activities that occur between the conclusion
of fieldwork and the issuance of the final auditor's report.  Relevant standards
include ISA 260 / SA 260 (Communication with TCWG), ISA 265 / SA 265
(Communicating Deficiencies), ISA 450 / SA 450 (Evaluation of Misstatements),
ISA 580 / SA 580 (Written Representations), and ISA 700 / SA 700
(Forming an Opinion).

The worksheets in this module cover the following phase activities:

1. **Draft Financial Statements (e59c663)** — Worksheet for reviewing the
   client's draft financial statements prior to signing the audit opinion.
   Ensures the statements are in acceptable form before the opinion is
   finalised.
2. **Management Letter (ae598e6)** — Documents findings and control
   deficiencies that have been escalated from the Audit Result Discussion
   (WR.110.4 / bc3e272) and are to be formally communicated to management
   in writing, as required by ISA 265 / SA 265.
3. **Management Representation (bbbdfe7)** — A checklist-based worksheet for
   obtaining and documenting management's written representations as required
   by ISA 580 / SA 580.  Each representation item is traceable with a
   response, comments, and supporting attachments.
4. **Final Discussion (de69c2f)** — A checklist-driven final-review worksheet
   that guides the engagement team through the pre-issuance quality checks and
   confirms that all significant outstanding matters have been resolved.
5. **Report Formatting Control (b555edd)** — Quality-control worksheet for
   checking the formatting, grammar, and layout of the draft auditor's report
   before it is submitted for partner sign-off.
6. **Audit Result (ff42fdc)** — Records and formalises the final audit opinion
   (``financial_statement_opinion_id``) and opinion date
   (``financial_statement_opinion_date``), providing the audit file with a
   definitive record of the opinion type issued.

**Key features:**

- Management Letter is auto-populated from escalated items in the Audit Result
  Discussion worksheet (bc3e272), covering both findings and control deficiencies
- Management Representation checklist is customisable via item master records
- Final Discussion checklist supports pre-issuance quality review
- Opinion type and date are linked back to the General Audit record
- Follows the standard worksheet workflow: Draft → Open → Confirm → Done

**Models:**

- ``general_audit_ws_ae598e6``           — Management Letter
- ``general_audit_ws_ae598e6.influence`` — Finding line in Management Letter
- ``general_audit_ws_ae598e6.control``   — Control deficiency line in Management Letter
- ``general_audit_ws_b555edd``           — Report Formatting Control
- ``general_audit_ws_bbbdfe7``           — Management Representation
- ``general_audit_ws_bbbdfe7.checklist`` — Representation checklist line
- ``general_audit_ws_bbbdfe7.item``      — Representation checklist item master
- ``general_audit_ws_de69c2f``           — Final Discussion
- ``general_audit_ws_de69c2f.checklist`` — Final discussion checklist line
- ``general_audit_ws_de69c2f.item``      — Final discussion checklist item master
- ``general_audit_ws_e59c663``           — Draft Financial Statements
- ``general_audit_ws_ff42fdc``           — Audit Result (opinion formalisation)

**ISA / SA references:** ISA 260 / SA 260 — Communication with TCWG;
ISA 265 / SA 265 — Communicating Deficiencies in Internal Control;
ISA 450 / SA 450 — Evaluation of Misstatements Identified during the Audit;
ISA 580 / SA 580 — Written Representations;
ISA 700 / SA 700 — Forming an Opinion and Reporting on Financial Statements;
ISA 705 / SA 705 — Modifications to the Opinion in the Independent Auditor's Report


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-general-audit
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *General Audit Worksheet - Draft Reporting*
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
