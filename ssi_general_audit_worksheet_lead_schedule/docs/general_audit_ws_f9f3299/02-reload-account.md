# Reload Accounts - Lead Schedule - Account

> **Module:** `ssi_general_audit_worksheet_lead_schedule`\
> **Model:** `general_audit_ws_f9f3299`\
> **Menu:** Risk Responses > Result > Lead Schedules\
> **Actor:** user in group _Lead Schedule - Account (f9f3299) — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`).
- **Data:** The **Standard Account Type** field is filled, and the parent General Audit
  has accounts of that type.
- **Access:** User is in group _Lead Schedule - Account (f9f3299) — User_ or higher.

## Flow

1. Open the **Risk Responses > Result > Lead Schedules** menu. If **Result** is not
   visible in the top menu bar, click the **+** button at its right end first.
2. Open the worksheet to work on.
3. Open the **Accounts** tab.
4. Click the **Reload** button. The button is only visible while the status is **On
   Progress**.

## Post-Condition

- The tab has one line for every account of the selected type that had none.
- Lines whose account left that type are removed.
- Other lines keep their manual input, and clicking **Reload** again changes nothing.
