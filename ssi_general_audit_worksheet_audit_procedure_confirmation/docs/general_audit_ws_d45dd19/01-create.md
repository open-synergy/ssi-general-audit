# Create Confirmation Audit Procedure

> **Module:** `ssi_general_audit_worksheet_audit_procedure_confirmation`\
> **Model:** `general_audit_ws_d45dd19`\
> **Menu:** Risk Responses > General Procedures > Confirmation\
> **Actor:** user in group _Confirmation Audit Procedure (d45dd19) — User_\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A `general_audit` record exists and is in status **Open**.
- **Access:** User is in group _Confirmation Audit Procedure (d45dd19) — User_ or
  higher.

## Flow

1. Open the **Risk Responses > General Procedures > Confirmation** menu. If **General
   Procedures** is not visible in the top menu bar, click the **+** button at its right
   end first. The menu list that opens shows **General Procedures** with its entries
   below it.
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

- **Open Confirmations** (on the **Confirmations** page of the form) only opens the list
  of confirmation requests of this worksheet; it changes no data.
- **Open Confirmation Details** (on a confirmation form) only opens the list of detail
  lines of that confirmation; it changes no data.
- **Generate Data** (on a confirmation detail form) recomputes the data of that detail
  line. The detail model is a child of a confirmation and has no work instruction of its
  own.
