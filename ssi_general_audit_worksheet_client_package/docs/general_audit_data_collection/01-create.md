# Create Data Collection

> **Module:** `ssi_general_audit_worksheet_client_package`\
> **Model:** `general_audit_data_collection`\
> **Menu:** Configuration > Standard & Regulation > Data Collections > Data Collections\
> **Actor:** user in group _Data Collection_\
> **State:** `—` → `—`

## Pre-Condition

- **Data:** At least one **Data Collection Category** and one **Client Account Type**
  exist.
- **Access:** User is in group _Data Collection_.

## Flow

1. Open the **Configuration > Standard & Regulation > Data Collections > Data
   Collections** menu. If **Standard & Regulation** is not visible in the top menu bar,
   click the **+** button at its right end first. The menu list that opens shows
   **Standard & Regulation** with its entries below it.
2. Click the **Create** button. _(16.0 and later: "New")_
3. Fill in the required fields:
   - **Name**: name of the data to collect.
   - **Code**: unique identifier. Type `/` if no identifier is needed.
   - **Type**: **Account Type** (default) or **Others**.
   - **Account Type**: select the client account type. It is shown and required only
     when **Type** is **Account Type**; it is cleared when **Type** is changed to
     **Others**.
   - **Category**: select the data collection category.
4. Click **Save**.

## Post-Condition

- A new Data Collection is created and is **Active**.
- The record shows the chosen **Type**, **Account Type** (for type **Account Type**) and
  **Category**.
