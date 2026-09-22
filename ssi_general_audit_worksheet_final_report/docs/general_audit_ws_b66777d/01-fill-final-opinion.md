# Fill Final Audit Opinion — Independen Auditor Report (b66777d)

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
- **Data:** For the **Populate** button to fill in a value, the same engagement (General
  Audit) must already have a **Proposed Audit Opinion** worksheet (`fc75636`, module
  `ssi_general_audit_worksheet_review`) with its **Draft Audit Opinion** tab filled in.
  When there is no such worksheet yet, Populate does nothing (no error) and the fields
  stay as they are.

## Flow

1. Open the **Windup & Reporting > Final Report > Independen Auditor Report** menu.
2. Open the worksheet to fill the final audit opinion for.
3. Open the **Final Audit Opinion** tab (placed right after the **Details** tab).
4. Click **Populate**. This copies the nine narrative fields from the same engagement's
   Proposed Audit Opinion worksheet's Draft Audit Opinion tab, when one exists.
5. Review and, if needed, edit any of the nine narrative fields. All are optional and
   always editable, whether or not Populate was clicked first, and regardless of the
   worksheet's status:
   - **Opinion**: Final narrative of the Opinion paragraph.
   - **Basis for Opinion**: Final narrative of the Basis for Opinion paragraph.
   - **Key Audit Matters**: Final narrative of the Key Audit Matters paragraph. Only
     relevant for engagements that require this section.
   - **Other Information**: Final narrative of the Other Information paragraph. Only
     relevant when the engagement includes other information.
   - **Responsibilities of Management**: Final narrative of the Responsibilities of
     Management paragraph.
   - **Auditor's Responsibilities**: Final narrative of the Auditor's Responsibilities
     paragraph.
   - **Report on Other Legal and Regulatory Requirements**: Final narrative of this
     section. Only relevant when such requirements apply.
   - **Emphasis of Matter**: Final narrative of the Emphasis of Matter paragraph. Only
     relevant when this paragraph is needed.
   - **Other Matter**: Final narrative of the Other Matter paragraph. Only relevant when
     this paragraph is needed.
6. Click **Save**.

## Post-Condition

- The nine Final Audit Opinion fields hold either the values copied by Populate, the
  manual edits made afterwards, or both, including any HTML markup (bold, bullet lists,
  etc.) used while editing.
- The **Details** tab is unaffected.
- Clicking Populate again replaces all nine fields with a fresh copy from the same
  fc75636 worksheet, discarding any manual edits made since the last Populate.
