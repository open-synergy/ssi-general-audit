# Create Plausible Relationship Audit Procedure

> **Module:** `ssi_general_audit_worksheet_audit_procedure_analytic`\
> **Model:** `general_audit_ws_aa899baf`\
> **Menu:** Risk Responses > General Procedures > Analytical Procedures – Account >
> Plausible Relationship\
> **Actor:** user in group _Plausible Relationship Audit Procedure (aa899baf) — User_\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A `general_audit` record exists and is in status **Open**.
- **Access:** User is in group _Plausible Relationship Audit Procedure (aa899baf) —
  User_ or higher.

## Flow

1. Open the **Risk Responses > General Procedures > Analytical Procedures – Account >
   Plausible Relationship** menu. If **General Procedures** is not visible in the top
   menu bar, click the **+** button at its right end first. The menu list that opens
   shows **General Procedures** with its entries below it.
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

- The **Variables** page has an **Open Variables** button that opens the variables of
  this worksheet in a separate list.
- The **Relations** page has an **Open Relations** button that opens the relations of
  this worksheet in a separate list.
