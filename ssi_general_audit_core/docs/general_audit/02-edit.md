# Edit General Audit

> **Module:** `ssi_general_audit_core`\
> **Extends:** ssi_general_audit — model `general_audit`, aksi `02-edit`

## Additional Pre-Condition

- **Module:** `ssi_general_audit_core` is installed.
- **Config:** The system parameter `ssi_general_audit.max_number_of_cpa_license` is set
  to the number of CPA licenses the installation is allowed to use. When it is missing,
  the allowed number is `0`.

## Modified Validation

- Changing the **CPA** of a General Audit fails with a **Validation Error** when the
  number of different **CPA** values used across all General Audit records is greater
  than the value of `ssi_general_audit.max_number_of_cpa_license`.
- The error message shows the document type, the record ID, the current number of CPAs,
  and the allowed number.
- To recover, restore the previous **CPA** or select one already used by another General
  Audit, or ask the system administrator to increase the parameter value.
