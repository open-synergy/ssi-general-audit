# Open Draft Financial Statements

> **Module:** `ssi_general_audit_worksheet_draft_reporting`\
> **Model:** `general_audit_ws_e59c663`\
> **Menu:** Windup & Reporting > Draft Reporting > Draft Financial Statements\
> **Actor:** the worksheet's assigned user/reviewer, the linked General Audit's user/reviewer,
> a System Administrator, or a member of group _Draft Financial Statements (e59c663) — Validator_\
> **State:** `draft` → `open`\
> **Requires:** `01-create`\
> **Inline Actions:** `action_populate_checklist` (Populate)

## Pre-Condition

- **Record:** Status is **Draft**.
- **Config:** An active `policy.template` for this model grants `open_ok` for state
  `draft` to the actor.
- **Config:** An active `sequence.template` exists for this model (the document number
  is assigned when the worksheet is started).
- **Access:** User matches one of the personas listed under **Actor**.

## Flow

1. Open the **Windup & Reporting > Draft Reporting > Draft Financial Statements** menu.
2. Open the record to start.
3. Click the **Start** button.
4. Click **OK** on the confirmation dialog.
5. Open the **Checklist** tab.
6. Click the **Populate** button to generate the WR.160.1 completeness checklist rows
   from the `general_audit_ws_e59c663.item` master.
7. On the first checklist row, set the **Option** field (Present / Not Present / Not
   Applicable) to confirm the row can be answered.

## Post-Condition

- Status changes to **On Progress** (`open`).
- A document number is assigned to the worksheet (per the `sequence.template`
  configuration).
- The **Checklist** tab is populated with one row per active
  `general_audit_ws_e59c663.item` master record (48 items as shipped), each row's
  **Item** and code matching the master. Every row can be answered (**Option**: Present
  / Not Present / Not Applicable) and annotated with a **Comment**.
- Clicking **Populate** again does not duplicate existing rows; it only adds rows for
  items missing from the checklist and removes rows whose item is no longer active in
  the master.
