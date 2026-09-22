# View Final Team Allocations — Independen Auditor Report (b66777d)

> **Module:** `ssi_general_audit_worksheet_final_report`
>
> **Model:** `general_audit_ws_b66777d`
>
> **Menu:** Windup & Reporting > Final Report > Independen Auditor Report
>
> **Actor:** user in group _Independen Auditor Report (b66777d) — User_
>
> **State:** open

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Access:** User is in group _Independen Auditor Report (b66777d) — User_ (or higher).
- **Data:** For the **Populate** button to fill in rows, at least one worksheet of the
  same engagement (General Audit) must have its **Preparation Time** and/or **Review
  Time** filled in, its Responsible/Reviewer user must be linked to an Employee, and
  that worksheet must have a **Worksheet Type** whose Category is one of Pre-Engagement,
  Risk Assessment, Risk Responses, or Windup & Reporting (the same four phases as the
  Audit Working Plan) — otherwise its time is not attributable to any phase column. When
  none of this is the case, Populate leaves the table empty (no error).

## Flow

1. Open the **Windup & Reporting > Final Report > Independen Auditor Report** menu.
2. Open the worksheet to view the final team allocations for.
3. Open the **Final Team Allocations** tab (placed right after the **Final Audit
   Opinion** tab).
4. Click **Populate**. This replaces the table with one row per Team Member (Employee)
   who has Preparation Time and/or Review Time recorded on any worksheet of the same
   engagement, showing:
   - **Team Member**: the employee.
   - **Pre-Engagement Allocation**, **Risk Assessment Allocation**, **Risk Responses
     Allocation**, **Windup & Reporting Allocation**: sum of Preparation Time + Review
     Time, per phase, across this engagement's worksheets attributed to this Team Member
     — the phase of each worksheet comes from its own Worksheet Type Category.
   - **Total Allocation**: the sum of the four phase columns above.
   - **AWP Total Allocation**: this Team Member's planned total hours from the same
     engagement's Audit Working Plan, when available (0 otherwise).
   - **Difference vs AWP**: Total Allocation minus AWP Total Allocation.
   - The row's form view additionally shows the four AWP phase columns (AWP
     Pre-Engagement/Risk Assessment/Risk Responses/Windup & Reporting Allocation) the
     realized phase columns are compared against.
   - Because Populate always re-reads every worksheet's current data from scratch,
     clicking it again after Preparation/Review Time is filled in later (e.g. for an
     engagement that was already in progress when this feature was introduced) always
     picks up the latest values — this doubles as the "Reload" behaviour for stale data.
5. Review the table. All columns are read-only; there is no manual add/edit/delete on
   this tab.

## Post-Condition

- The **Final Team Allocations** table holds a fresh snapshot as of the last Populate
  click, one row per contributing Team Member.
- The **Final Audit Opinion** and **Details** tabs are unaffected.
- Clicking Populate again replaces the whole table with a fresh snapshot.
