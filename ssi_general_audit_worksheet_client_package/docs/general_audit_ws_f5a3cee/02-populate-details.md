# Populate Details — Data Collection

> **Module:** `ssi_general_audit_worksheet_client_package`\
> **Model:** `general_audit_ws_f5a3cee`\
> **Menu:** Risk Assessment > Client Assistance Package > Data Collection\
> **Actor:** user in group _Data Collection (f5a3cee) — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`). The button is hidden only in
  **Draft**.
- **Data:** The client of the General Audit has an account mapping with account types.
  Data Collection master items exist (Configuration > Standard & Regulation > Data
  Collections > Data Collections), each with type **Account Type**, **Permanent File**
  or **Current File**.
- **Access:** User is in group _Data Collection (f5a3cee) — User_ (or higher).

## Flow

1. Open the **Risk Assessment > Client Assistance Package > Data Collection** menu.
2. Open the worksheet to work on.
3. Open the **Details** tab. The tabs of the worksheet are **Primary**,
   **Permanent/Current** and **Details**, in that order.
4. Click the **Populate** button. The button is not visible while the status is
   **Draft**.
5. Click a line in **Details** to open it and review the data requested for that account
   type.
6. To attach files to a data line, click the **Upload Attachment** button at the end of
   the line, choose the files and click **Submit**. The files are added to the line and
   kept as attachments of the worksheet. The button is shown for saved lines while the
   status is **On Progress**.
7. Open the **Permanent/Current** tab to review the data that is not tied to an account
   type, listed under **Permanent File** and **Current File**.

## Post-Condition

- The **Details** tab has one line for every account type in the client's account
  mapping; existing lines are kept and lines whose account type is no longer mapped are
  removed. The list shows the account type only.
- Opening a **Details** line shows one data line for every active master item of type
  **Account Type** with that account type. The name is filled from the master item;
  Date, attachments and completion are filled in on these data lines. You can also add a
  line yourself by typing its name. Data lines without a master item are kept.
- A **Details** line is marked **Completed** automatically once all of its data lines
  are completed.
- The **Primary** tab holds **Reporting Timetable to be Followed by the Entity**, a list
  with **Description** and **Date** that you fill in yourself while the status is **On
  Progress**. Populate does not change it.
- The **Permanent/Current** tab holds the **Permanent File** list above the **Current
  File** list. Both have the same columns as the data lines. Each has one line for every
  active master item of its own type. Items of type **Primary** are not added to them.
  Lines you added yourself are kept.
- Lines you already filled in (date, attachments, completion) are not changed.
- Data lines whose master item was deactivated or changed are removed.
- Clicking **Populate** again does not duplicate lines.
