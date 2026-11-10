# Open Report Formatting Control

> **Module:** `ssi_general_audit_worksheet_draft_reporting`\
> **Model:** `general_audit_ws_b555edd`\
> **Menu:** Windup & Reporting > Draft Reporting > Report Formatting Control\
> **Actor:** the worksheet's assigned user/reviewer, the linked General Audit's user/reviewer,
> a System Administrator, or a member of group _Report Formatting Control (b555edd) — Validator_\
> **State:** `draft` → `open`\
> **Requires:** `01-create`\
> **Inline Actions:** `action_reload_account` (Reload)

## Pre-Condition

- **Record:** Status is **Draft**.
- **Config:** An active `policy.template` for this model grants `open_ok` for state
  `draft` to the actor.
- **Config:** An active `sequence.template` exists for this model (the document number
  is assigned when the worksheet is started).
- **Data:** The linked General Audit has standard account type lines, so Reload has
  something to show.
- **Access:** User matches one of the personas listed under **Actor**.

## Flow

1. Open the **Windup & Reporting > Draft Reporting > Report Formatting Control** menu.
2. Open the record to start.
3. Click the **Start** button.
4. Click **OK** on the confirmation dialog.
5. Open the **Statement of Comprehensive Income** tab, the first tab on the form. It
   stays empty until **Reload** is clicked.
6. Open the **Statement of Financial Position** tab, the second tab.
7. Click the **Reload** button to fill both statement tabs from the General Audit's
   standard account type lines.
8. Open the **Statement of Changes in Equity** tab. **Reload** also fills this tab, one
   row per equity component, first for the current period and then for the previous
   period.
9. Optionally type the owner transactions on a row: **Issuance of Shares**, **Treasury
   Shares**, **Addition of Reserves** and **Dividends**, entered as the amount that
   changes the component (a dividend is negative).
10. Open the **Statement of Cash Flows** tab. **Reload** also fills this tab, for the
    current period and, when the General Audit keeps one, the previous period.
11. Type in the rows that have no calculation, such as **Dividends paid** and **Gain on
    sale of fixed assets** (inflow positive, outflow negative). The totals and the
    **Difference** row refresh as soon as you save the amount.

## Post-Condition

- Status changes to **On Progress** (`open`).
- A document number is assigned to the worksheet (per the `sequence.template`
  configuration).
- **Statement of Comprehensive Income** lists the rows of account groups T009-T015
  (revenue, expenses and other comprehensive income), each with its **Current Balance**
  and **Previous Balance**.
- **Statement of Financial Position** lists one row per standard account type of the
  General Audit that belongs to account groups T001-T008 (assets, liabilities and
  equity), each with its **Current Balance** and **Previous Balance**. The **Retained
  Earnings - unappropriated** row shows the audited balance plus the net profit of the
  same period, so it agrees with the closing equity in the **Statement of Changes in
  Equity** tab. Other rows show the audited balance only. Once the closing lines of the
  General Audit are generated, the closing is the only source for the **Current
  Balance**: each destination account type adds its closing amount and the net profit is
  no longer added to the Retained Earnings row, so it is not counted twice. The
  **Previous Balance** is not affected.
- **Statement of Changes in Equity** lists, per period, one row per equity component
  with **Opening Balance**, **Profit**, **OCI**, the four owner transactions, **Other
  Movement** and **Closing Balance**. Profit goes to Retained Earnings and OCI to Other
  Comprehensive Income. **Other Movement** is the part of the movement that profit, OCI
  and the typed-in owner transactions do not explain; it becomes 0 once the owner
  transactions are filled in. The previous period section has rows only when the General
  Audit keeps a previous period. For the current period, **Closing Balance** is read
  from the **Worksheet** of the General Audit (its **Balance Sheet** column, including
  the closing that no account receives), so both statements agree; the newest Worksheet
  that is not cancelled or rejected and has lines is used. Without such a Worksheet, or
  for the previous period, it is the audited balance plus profit and OCI. Because the
  Worksheet already holds the profit, the profit also shows as **Other Movement** on the
  Retained Earnings row when it is not explained by the owner transactions.
- **Statement of Cash Flows** lists the operating (profit before tax, non-cash
  adjustments, working capital changes, interest and tax paid), investing and financing
  rows, then the total of each section, the net change in cash, the opening cash, the
  computed closing cash, the closing cash of the trial balance and their **Difference**.
  The method is indirect. An increase of an asset account is a cash outflow and an
  increase of a liability or equity account is a cash inflow. A **Difference** other
  than 0 means some cash movement is not mapped to a row yet; the mapping is kept in
  **Configuration > Account & Computation > Cash Flow Item**.
- Clicking **Reload** never asks for confirmation and never clears figures you typed in.
  It refreshes only the figures that come from the General Audit: the account balances,
  the opening balance, profit, OCI and closing balance of the equity rows, and the
  calculated cash flow rows. The owner transactions on the equity rows and the amounts
  of the cash flow rows without a calculation (for example **Dividends paid**) keep the
  values you typed in.
- Clicking **Reload** again does not duplicate rows; it adds the rows that are missing,
  removes the rows that no longer belong (for example the previous period rows after the
  General Audit stops keeping a previous period) and keeps the others. **Reload** is
  visible only while the worksheet is **Draft** or **On Progress**.
