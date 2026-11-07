# Generate Sampling - Sample Determination

> **Module:** `ssi_general_audit_worksheet_sample_determination`\
> **Model:** `general_audit_ws_a916660`\
> **Menu:** Risk Responses > Substantive Test > Sample Determination\
> **Actor:** user in group _Sample Determination (a916660) — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`).
- **Data:** **Data Mode** and its source (**General Ledger** or **Subledger**) are
  selected, and the **Identifier** and **Monetary** column numbers are filled on the
  **Data** tab.
- **Data:** The inputs and parameters of the selected **Sampling Method** are filled in,
  so that the sampling interval (Monetary Unit Sampling), the computed sample size
  (Classical Variable Sampling), or the sample pool (Non-Statistical Sampling) is
  greater than zero.
- **Access:** User is in group _Sample Determination (a916660) — User_ or higher.

## Flow

1. Open the **Risk Responses > Substantive Test > Sample Determination** menu. If
   **Substantive Test** is not visible in the top menu bar, click the **+** button at
   its right end first.
2. Open the worksheet to work on.
3. Open the **Data** tab.
4. Click the **Generate Sampling** button. The button is only visible while the status
   is **On Progress**.
5. Open the **Sampling Data** tab to review the result.

## Post-Condition

- The **Sampling Data** tab lists the key items (100% examination) first, followed by
  the sample items selected by the chosen method.
- For Non-Statistical Sampling, no sample is selected automatically: the remaining items
  are listed as candidates in the **Sampling Process** tab, where you tick **Chose?** to
  pick them.
- If the source, the column numbers, or the method inputs are incomplete, the **Sampling
  Data** tab is emptied instead.
- Clicking the button again redraws the sampling and replaces the previous result.
