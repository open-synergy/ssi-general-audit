.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================================================
General Audit Worksheet - Vouching Audit Procedure
==================================================

This module provides the worksheet for documenting **vouching** audit
procedures, in accordance with ISA 500 / SA 500 (Audit Evidence).

Vouching is a substantive audit procedure where the auditor traces from
recorded transactions back to supporting source documents (e.g., invoices,
purchase orders, contracts, receipts) to verify the accuracy, completeness,
and validity of recorded amounts.  The procedure provides evidence that
recorded transactions actually occurred and are properly authorized.

Typical use cases include:

- Verifying recorded revenue by tracing sales entries to customer invoices
  and delivery notes
- Confirming recorded expenses by tracing journal entries to vendor invoices
  and payment authorizations
- Validating fixed-asset additions by tracing to purchase orders and supplier
  invoices

**Key features:**

- Links each vouching worksheet to a specific audit area via the Key Audit
  Procedures worksheet (Lead Schedule / WS-E51BB1C)
- Associates the worksheet with relevant financial statement assertions
  (e.g., Existence, Rights & Obligations, Completeness, Accuracy)
- Ties the worksheet to the relevant standard account type being audited
- Captures population description and sampling approach
- Records audit findings from the vouching procedure
- Follows the standard worksheet workflow: Draft → Open → Confirm → Done

**Models:**

- ``general_audit_ws_b4f7d9c`` — Main vouching worksheet

**ISA / SA references:** ISA 500, SA 500 — Audit Evidence


Installation
============

To install this module, you need to:

#. Clone the ``ssi-general-audit`` repository.
#. Add the path to your Odoo ``addons_path``.
#. Install the module via the Odoo Apps interface or via command line.


Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/open-synergy/ssi-general-audit/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smash it by providing a detailed and welcomed
`feedback <https://github.com/open-synergy/ssi-general-audit/issues/new?body=module:%20ssi_general_audit_worksheet_audit_procedure_vouching%0Aversion:%2014.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.


Credits
=======

Authors
~~~~~~~

* OpenSynergy Indonesia
* PT. Simetri Sinergi Indonesia

Contributors
~~~~~~~~~~~~

* PT. Simetri Sinergi Indonesia <dev@simetri-sinergi.id>

Maintainers
~~~~~~~~~~~

This module is maintained by PT. Simetri Sinergi Indonesia.
