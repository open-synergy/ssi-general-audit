# Fill Checklist — Final Communication With TCWG (f3ed115)

> **Module:** `ssi_general_audit_worksheet_final_report`
>
> **Model:** `general_audit_ws_f3ed115`
>
> **Menu:** Windup & Reporting > Final Report > Final Communication With TCWG
>
> **Actor:** user in group _Audit Report (f3ed115) — User_
>
> **State:** open

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Access:** User is in group _Audit Report (f3ed115) — User_ (or higher).
- **Data:** The checklist master data (4 categories, 15 items) is installed with the
  module. Only active items are listed by **Populate**. Every item offers the options
  Present, Not Present and Not Relevant.

## Flow

1. Open the **Windup & Reporting > Final Report > Final Communication With TCWG** menu.
2. Open the worksheet to fill the checklist for.
3. Open the **Checklist** tab.
4. Click **Populate**. This creates one row per active checklist item, ordered by
   category and then by item. Rows that already exist are kept as they are, and rows
   whose item is no longer in the master data are removed.
5. Click **Edit** to make the worksheet editable.
6. Click a row to open it, then choose the **Option** (Present, Not Present or Not
   Relevant) for that item.
7. Click **Save & Close** to return to the table. Repeat steps 6 and 7 for each item.
8. Click **Save**.

## Post-Condition

- The **Checklist** tab lists 15 rows, one per checklist item, each showing the
  **Option** that was chosen (empty for rows not yet answered).
- Clicking **Populate** again does not duplicate any row.
- When the worksheet is no longer **On Progress**, the **Populate** button is hidden and
  rows cannot be created or deleted from the table.
