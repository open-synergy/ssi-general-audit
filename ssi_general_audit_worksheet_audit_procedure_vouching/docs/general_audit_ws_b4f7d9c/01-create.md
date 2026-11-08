# Create Vouching Audit Procedure

> **Module:** `ssi_general_audit_worksheet_audit_procedure_vouching`\
> **Model:** `general_audit_ws_b4f7d9c`\
> **Menu:** Risk Responses > General Procedures > Inspection > Vouching\
> **Actor:** user in group _Vouching Audit Procedure (b4f7d9c) — User_\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A `general_audit` record exists and is in status **Open**.
- **Access:** User is in group _Vouching Audit Procedure (b4f7d9c) — User_ or higher.

## Flow

1. Open the **Risk Responses > General Procedures > Inspection > Vouching** menu. If
   **General Procedures** is not visible in the top menu bar, click the **+** button at
   its right end first. The menu list that opens shows **General Procedures** with its
   entries below it.
2. Click the **Create** button. _(16.0 and later: "New")_
3. Fill in the required field:
   - **General Audit**: select the open `general_audit` engagement this worksheet
     belongs to.
4. **Accountant**, **Partner**, and **Title** are automatically filled from the selected
   **General Audit**.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.

## Related Views

- **Open Data Comparisons** (on the **Data Comparisons** page of the form) only opens
  the list of data comparison sources of this worksheet; it changes no data.
- **Open Vouching Lines** (on the **Vouching** page of the form) only opens the list of
  vouching lines of this worksheet; it changes no data.
- **Compute Vouching Data** (on a vouching line form) recomputes the vouching result of
  that line. The vouching line model is a child of the worksheet and has no work
  instruction of its own.
