.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================================================
General Audit Worksheet - Inquiry Audit Procedure
=================================================

This module provides the worksheet for documenting **inquiry** audit
procedures, as required by ISA 500 / SA 500 (Audit Evidence) and ISA 240 /
SA 240 (The Auditor's Responsibilities Relating to Fraud).

Inquiry is one of the fundamental audit procedures used to collect audit
evidence by seeking information from knowledgeable persons — both financial
and non-financial — inside or outside the entity being audited. Responses to
inquiries may corroborate other evidence, provide new information, or indicate
where further investigation is needed.

**Key features:**

- Links each inquiry session to a specific audit area via the Key Audit
  Procedures worksheet (Lead Schedule / WS-E51BB1C)
- Associates the inquiry with relevant financial statement assertions
  (e.g., Existence, Rights & Obligations, Completeness, Accuracy)
- Ties the inquiry to the relevant standard account type being audited
- Records the source of information (person/party being inquired) and their
  position/role within the entity
- Supports a structured Q&A list (``general_audit_ws_a145276.question``) so
  that each question posed and each answer received are individually documented
- Captures background context and a summary of findings
- Records an overall risk assessment (Low / Medium / High) derived from the
  inquiry responses
- Follows the standard worksheet workflow: Draft → Open → Confirm → Done

**Models:**

- ``general_audit_ws_a145276`` — Main inquiry worksheet header
- ``general_audit_ws_a145276.question`` — Individual question-and-answer lines
  within an inquiry worksheet

**ISA / SA references:** ISA 500, SA 500 — Audit Evidence;
ISA 240, SA 240 — The Auditor's Responsibilities Relating to Fraud in an
Audit of Financial Statements


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-general-audit
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *General Audit Worksheet - Inquiry Audit Procedure*
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
