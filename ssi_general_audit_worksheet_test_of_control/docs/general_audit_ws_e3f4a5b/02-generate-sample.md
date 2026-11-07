# Generate Sample - Test of Control

> **Module:** `ssi_general_audit_worksheet_test_of_control`\
> **Model:** `general_audit_ws_e3f4a5b`\
> **Menu:** Risk Assessment > Control Risk > Test of Controls\
> **Actor:** user in group _Test of Control (e3f4a5b) — User_

## Pre-Condition

- **Record:** The worksheet exists and its **Data Mode** and data source (**General
  Ledger** or **Subledger**) are selected, so that the **Raw Data** tab is filled.
- **Data:** At least one control attribute exists in the **Attribute Sampling** tab, so
  that **Sample Actual** is greater than zero.
- **Access:** User is in group _Test of Control (e3f4a5b) — User_ or higher.

## Flow

1. Open the **Risk Assessment > Control Risk > Test of Controls** menu. If **Control
   Risk** is not visible in the top menu bar, click the **+** button at its right end
   first.
2. Open the worksheet to work on.
3. Open the **Sample Data** tab.
4. Click the **Generate Sample** button.
5. Review the generated rows in the **Sample Data** tab.

## Post-Condition

- The **Sample Data** tab lists randomly selected rows from the raw data. The number of
  rows is **Sample Actual**, or the population size if that is smaller.
- The same sample is passed on to every control attribute, which gets its own **Sample
  Data** with an extra **Deviation** column.
- If the raw data is empty or **Sample Actual** is zero, an error message is shown and
  nothing changes.
- Clicking the button again draws a new random sample and replaces the previous one.
