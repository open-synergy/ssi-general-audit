# Compute Deviation - Test of Control

> **Module:** `ssi_general_audit_worksheet_test_of_control`\
> **Model:** `general_audit_ws_e3f4a5b`\
> **Menu:** Risk Assessment > Control Risk > Test of Controls\
> **Actor:** user in group _Test of Control (e3f4a5b) — User_

## Pre-Condition

- **Record:** The worksheet has a control attribute whose **Sample Data** was generated
  (see `02-generate-sample.md`).
- **Data:** The deviating items are marked in the **Deviation** column of the attribute
  sample table.
- **Access:** User is in group _Test of Control (e3f4a5b) — User_ or higher.

## Flow

1. Open the **Risk Assessment > Control Risk > Test of Controls** menu. If **Control
   Risk** is not visible in the top menu bar, click the **+** button at its right end
   first.
2. Open the worksheet to work on.
3. Open the **Attribute Sampling** tab and click **Open Attributes**. The list of the
   worksheet's control attributes opens.
4. Open the attribute to evaluate.
5. Open the **Sample Data** tab and click the **Compute Deviation** button.

## Post-Condition

- **Sample Actual** shows the number of rows in the attribute sample table.
- **Deviation Count** shows the number of rows marked as deviating.
- Clicking **Generate Sample** on the attribute form instead rebuilds that attribute's
  sample table from the worksheet sample.
