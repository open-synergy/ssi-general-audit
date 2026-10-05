# Fill Final Audit Opinion — Proposed Audit Opinion (fc75636)

> **Module:** `ssi_general_audit_worksheet_review`
>
> **Model:** `general_audit_ws_fc75636`
>
> **Menu:** Windup & Reporting > Final Report > Proposed Audit Opinion
>
> **Actor:** user in group _Independen Auditor Report (fc75636) — User_
>
> **State:** open

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Access:** User is in group _Independen Auditor Report (fc75636) — User_ (or higher).
- **Data:** At least one audit opinion exists in the list of opinions to choose from.

## Flow

1. Open the **Windup & Reporting > Final Report > Proposed Audit Opinion** menu.
2. Open the worksheet to fill the final audit opinion for.
3. Click the **Edit** button.
4. In the section right above **Conclusion**, fill in:
   - **Final Audit Opinion**: Choose the audit opinion for the engagement, from the same
     opinions used by the Audit Final Memorandum.
   - **Final Opinion Date**: Enter the date of the audit opinion.
5. Click **Save**.

## Post-Condition

- **Final Audit Opinion** and **Final Opinion Date** keep the values entered.
- The Independent Auditor Report of the same engagement shows them as **Audit Opinion**
  and **Opinion Date** (read-only), right above its **Conclusion**.
- Once that Independent Auditor Report is On Progress or Done, the **Opinion** and
  **Opinion Date** of the General Audit show the same values and can no longer be
  edited. Until then, and whenever the report has no opinion, they stay empty.
