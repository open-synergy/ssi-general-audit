.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================================================
General Audit Worksheet - Inspection
=================================================

This module provides the worksheet for documenting **physical check**
(physical inspection) audit procedures, in accordance with ISA 501 (Audit
Evidence -- Specific Considerations for Selected Items).

Physical check is a substantive audit procedure where the auditor directly
inspects tangible assets -- e.g. fixed assets, inventory -- to verify their
existence, condition, and completeness against recorded amounts. It
mirrors the Vouching Audit Procedure worksheet's Data Mode / Data
Comparison / Check Line structure, but where Vouching traces recorded
transactions back to supporting *documents*, Physical Check compares
recorded amounts against a *physical* count or observation.

Typical use cases include:

- Observing physical inventory counts and comparing the counted
  quantity/value to the recorded inventory ledger
- Physically inspecting fixed assets (e.g. property, plant and equipment)
  to confirm existence and condition against the fixed asset register

**Key features:**

- Links each physical check worksheet to a specific audit area via the Key
  Audit Procedures worksheet (Lead Schedule / WS-E51BB1C)
- Associates the worksheet with relevant financial statement assertions
  (e.g., Existence, Completeness)
- Ties the worksheet to the relevant standard account type being audited
- Selects a population from General Ledger or Subledger worksheets (Data
  Mode), optionally narrowed to a Sample Determination worksheet's sample
  (Data Source)
- Records one or more comparison data sources (Data Comparison) and
  compares them against the population using count/sum/avg aggregation
  (Check Line)
- Captures population description, sampling approach, and findings
- Follows the standard worksheet workflow: Draft -> Open -> Confirm -> Done

**Models:**

- ``general_audit_ws_c7d5f2b`` -- Main physical check worksheet
- ``general_audit_ws_c7d5f2b.data_comparison`` -- Comparison data source
  lines
- ``general_audit_ws_c7d5f2b.check_line`` -- Physical check comparison
  lines

**ISA / SA references:** ISA 501 -- Audit Evidence, Specific
Considerations for Selected Items


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
`feedback <https://github.com/open-synergy/ssi-general-audit/issues/new?body=module:%20ssi_general_audit_worksheet_physical_check%0Aversion:%2014.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

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
