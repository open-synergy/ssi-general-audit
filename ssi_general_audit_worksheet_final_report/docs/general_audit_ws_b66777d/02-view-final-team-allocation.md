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
  Time** filled in, and its Responsible/Reviewer user must be linked to an Employee.
  When neither is the case, Populate leaves the table empty (no error).

## Flow

1. Open the **Windup & Reporting > Final Report > Independen Auditor Report** menu.
2. Open the worksheet to view the final team allocations for.
3. Open the **Final Team Allocations** tab (placed right after the **Final Audit
   Opinion** tab).
4. Click **Populate**. This replaces the table with one row per Team Member (Employee)
   who has Preparation Time and/or Review Time recorded on any worksheet of the same
   engagement, showing:
   - **Team Member**: the employee.
   - **Total Preparation Time**: sum of Preparation Time across this engagement's
     worksheets prepared by this Team Member.
   - **Total Review Time**: sum of Review Time across this engagement's worksheets
     reviewed by this Team Member.
   - **Total Allocation**: Total Preparation Time + Total Review Time.
   - **AWP Total Allocation**: this Team Member's planned total hours from the same
     engagement's Audit Working Plan, when available (0 otherwise).
   - **Difference vs AWP**: Total Allocation minus AWP Total Allocation.
5. Review the table. All columns are read-only; there is no manual add/edit/delete on
   this tab.

## Post-Condition

- The **Final Team Allocations** table holds a fresh snapshot as of the last Populate
  click, one row per contributing Team Member.
- The **Final Audit Opinion** and **Details** tabs are unaffected.
- Clicking Populate again replaces the whole table with a fresh snapshot.
