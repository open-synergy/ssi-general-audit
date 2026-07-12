.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===================================================================
General Audit Worksheet - Understanding Entity and It's Environment
===================================================================

This module provides worksheets for the **Understanding of the Entity and Its
Environment** phase of a general audit engagement, in accordance with:

- **ISA 315 (Revised) / SA 315** — Identifying and Assessing the Risks of Material Misstatement
- **ISA 240 / SA 240** — The Auditor's Responsibilities Relating to Fraud
- **ISA 250 / SA 250** — Consideration of Laws and Regulations
- **ISA 402 / SA 402** — Audit Considerations Relating to an Entity Using a Service Organisation
- **ISA 550 / SA 550** — Related Parties
- **ISA 570 (Revised) / SA 570** — Going Concern
- **ISA 620 / SA 620** — Using the Work of an Auditor's Expert

ISA 315 requires auditors to obtain a sufficient understanding of the entity and its
environment, including its internal control, to identify and assess risks of material
misstatement. This module captures that understanding through a set of structured,
linked worksheets that together form the entity understanding working paper file.

Worksheets Covered
==================

- **WS: Understanding Summary (f87b2e1)** — Master summary worksheet linking all
  individual understanding worksheets. Provides the auditor with a single view of
  all understanding inputs and their completion status.
- **WS: General Information and Legal Aspect (ddf034c)** — RA.150.1: Legal structure,
  deed of establishment, management/shareholder composition, ownership of locations,
  and client contact persons.
- **WS: Structure Organization and Responsibilities (e78a3c6)** — RA.150.2:
  Organizational hierarchy, department responsibilities, and org chart image.
- **WS: Main Business Activity Process (ae11f7e)** — RA.150.3: Business cycles, key
  customers, suppliers, competitors, related parties, investments, funding, experts,
  outsourced services, and accounting policies.
- **WS: Business Cycle Summaries (a604795)** — RA.150.4: Transaction classes per
  business cycle, business functions, associated documents, and assigned team members.
- **WS: Business Environment (bdcdfc5)** — RA.150.5: External business environment
  factors (industry, economic, regulatory, technological) and their financial statement
  impacts.
- **WS: Financial Statement Preparation (f6a227)** — RA.150.6: How financial statements
  are prepared step-by-step, control activities per step, and potential misstatements.
- **WS: Relevant Regulations (a13a30e)** — RA.150.7: Laws and regulations applicable
  to the entity and their significant impact on financial reporting (ISA 250).
- **WS: Going Concern — Preliminary (c0d0898)** — RA.150.8: Preliminary assessment of
  going concern indicators at the planning stage (ISA 570).
- **WS: Fraud Factor Analysis (c0e0eec)** — Fraud risk indicator assessment structured
  around the fraud triangle (ISA 240): TCGW, management, and other evidence.

Key Features
============

- Comprehensive, linked worksheets covering all ISA 315 understanding dimensions
- Fraud risk indicators auto-populated from configurable master list (ISA 240)
- Going concern indicators auto-populated from master list (ISA 570)
- Business cycle and transaction class documentation with business function mapping
- Expert engagement documentation and type classification (ISA 620)
- Impact flags on standard account details: regulation, fraud, business environment,
  expert, going concern, and FS preparation
- All worksheets follow the standard ``general_audit_worksheet_mixin`` architecture

Models
======

**Worksheets**

+---------------------------------------------------------+-----------------------------------------------------+
| Model                                                   | Description                                         |
+=========================================================+=====================================================+
| ``general_audit_ws_f87b2e1``                            | WS: Understanding Summary (cross-links all below)   |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_ddf034c``                            | WS: General Information and Legal Aspect (RA.150.1) |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_ddf034c.contact``                    | General Info — client contact person                |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_ddf034c.ownership``                  | General Info — ownership status per location        |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_ddf034c.est_composition``            | General Info — management composition (deed)        |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_ddf034c.adm_composition``            | General Info — management composition (amendment)   |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_ddf034c.est_shareholding``           | General Info — shareholding structure (deed)        |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_ddf034c.adm_shareholding``           | General Info — shareholding structure (amendment)   |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_e78a3c6``                            | WS: Structure Organization & Responsibilities       |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_e78a3c6.organization_structure``     | Org Structure — organization unit line              |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_ae11f7e``                            | WS: Main Business Activity Process (RA.150.3)       |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_ae11f7e.related_party``              | Main Business — related party entry                 |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_ae11f7e.other_investment``           | Main Business — other investment entry              |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_ae11f7e.primary_funding``            | Main Business — primary funding source              |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_ae11f7e.customer``                   | Main Business — key customer                        |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_ae11f7e.supplier``                   | Main Business — key supplier                        |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_ae11f7e.competitor``                 | Main Business — key competitor                      |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_ae11f7e.expert``                     | Main Business — expert engagement record            |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_ae11f7e.other_provided_service``     | Main Business — outsourced service                  |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_ae11f7e.accounting_policy``          | Main Business — relevant accounting policy          |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_ae11f7e.other_evidence``             | Main Business — other audit evidence                |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_ae11f7e.other_information``          | Main Business — other significant information       |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_ae11f7e.previous_audit_evidence``    | Main Business — prior audit evidence                |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_ae11f7e.previous_audit_information`` | Main Business — prior audit information             |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_ae11f7e.previous_other_information`` | Main Business — prior other information             |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_a604795``                            | WS: Business Cycle Summaries (RA.150.4)             |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_a604795.detail``                     | Business Cycle — transaction class detail           |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_a604795.business_function``          | Business Cycle — business function line             |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_bdcdfc5``                            | WS: Business Environment (RA.150.5)                 |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_bdcdfc5.detail``                     | Business Environment — assessment detail line       |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_f6a227``                             | WS: FS Preparation Understanding (RA.150.6)         |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_f6a227.detail``                      | FS Preparation — preparation step detail line       |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_a13a30e``                            | WS: Relevant Regulations (RA.150.7)                 |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_a13a30e.detail``                     | Regulations — regulation assessment line            |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_c0d0898``                            | WS: Going Concern Preliminary (RA.150.8)            |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_c0d0898.detail``                     | Going Concern — indicator assessment line           |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_c0e0eec``                            | WS: Fraud Factor Analysis                           |
+---------------------------------------------------------+-----------------------------------------------------+
| ``general_audit_ws_c0e0eec.detail``                     | Fraud Factor — indicator assessment line            |
+---------------------------------------------------------+-----------------------------------------------------+

**Master Data**

+------------------------------------------+------------------------------------------------+
| Model                                    | Description                                    |
+==========================================+================================================+
| ``general_audit_class_transaction``      | Master: Class of Transaction                   |
+------------------------------------------+------------------------------------------------+
| ``general_audit_business_function``      | Master: Business Function                      |
+------------------------------------------+------------------------------------------------+
| ``general_audit_business_document``      | Master: Business Document                      |
+------------------------------------------+------------------------------------------------+
| ``accounting_application``               | Master: Accounting Application / IT System     |
+------------------------------------------+------------------------------------------------+
| ``general_audit_expert_type``            | Master: Expert Type                            |
+------------------------------------------+------------------------------------------------+
| ``general_audit_fraud_factor_category``  | Master: Fraud Factor Category (fraud triangle) |
+------------------------------------------+------------------------------------------------+
| ``general_audit_fraud_factor``           | Master: Fraud Factor                           |
+------------------------------------------+------------------------------------------------+
| ``general_audit_fraud_factor_indicator`` | Master: Fraud Factor Indicator                 |
+------------------------------------------+------------------------------------------------+
| ``general_audit_fs_preparation_step``    | Master: Financial Statement Preparation Step   |
+------------------------------------------+------------------------------------------------+
| ``general_audit_going_concern_category`` | Master: Going Concern Category                 |
+------------------------------------------+------------------------------------------------+
| ``general_audit_going_concern``          | Master: Going Concern Indicator                |
+------------------------------------------+------------------------------------------------+
| ``general_audit_other_report``           | Master: Other Report Type                      |
+------------------------------------------+------------------------------------------------+
| ``ownership_location``                   | Master: Ownership Location                     |
+------------------------------------------+------------------------------------------------+

Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-general-audit
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *General Audit Worksheet - Understanding Entity and It's Environment*
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
