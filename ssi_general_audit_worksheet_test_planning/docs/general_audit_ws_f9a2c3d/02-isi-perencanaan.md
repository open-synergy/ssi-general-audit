# Fill In the Planning — Test of Detail Planning (f9a2c3d)

> **Module:** `ssi_general_audit_worksheet_test_planning`\
> **Model:** `general_audit_ws_f9a2c3d`\
> **Menu:** Risk Responses > Substantive Test > Test of Detail Planning\
> **Actor:** user in group _Test of Detail Planning (f9a2c3d) — User_\
> **State:** `open`\
> **Requires:** `01-load-detail`

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Record:** The **Details** table has at least one line (see `01-load-detail`).
- **Data:** The **Test of Detail Timing**, **Test of Detail Extent** and **Primary Audit
  Technique** master data exist (the module installs three timings, two extents and
  seven techniques).
- **Access:** User is in group _Test of Detail Planning (f9a2c3d) — User_ (or higher).

## Flow

1. Open the **Risk Responses > Substantive Test > Test of Detail Planning** menu.
2. Open the worksheet to plan.
3. Open the **Details** tab (the first tab).
4. Click the **Timing** cell of the account line and choose a timing.
5. Click the **Extent** cell and choose an extent.
6. Click the **Primary Audit Technique** cell and choose a technique. Choose another
   technique in the same cell to add a second one.
7. Click **Save**.

## Post-Condition

- The line shows the chosen **Timing**, **Extent** and **Primary Audit Technique**.
- The other columns of the line are unchanged and cannot be edited.
- When the worksheet is no longer **On Progress**, the three columns cannot be edited.
