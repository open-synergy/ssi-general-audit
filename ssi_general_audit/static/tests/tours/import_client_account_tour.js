/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html). */

odoo.define("ssi_general_audit.import_client_account_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/import_client_account/01-import.md
    //
    // Flow 4-7 (select the CSV file, read the preview, click Import,
    // read the notification, check the new lines) are NOT driven by this
    // tour: the file upload dialog of the browser has no DOM completion
    // signal and can hang headless Chrome. The tour proves the Import
    // Accounts button opens the wizard with its File field, then closes
    // it with Cancel. The preview and the imported values are covered by
    // the unit tests in tests/test_import_client_account.py.
    tour.register(
        "ssi_general_audit_import_client_account_import",
        {
            test: true,
            url: "/web",
        },
        [
            // Flow 1 - Open Risk Assessment > Trial Balance > CoA and Mapping
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Risk Assessment app",
                trigger:
                    '.o_app[data-menu-xmlid="ssi_general_audit.menu_risk_assesment_root"]',
            },
            {
                content: "Open the Trial Balance menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_general_audit.menu_general_audit_trial_balance"]',
            },
            {
                content: "Open the CoA and Mapping menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_general_audit.client_account_mapping_menu"]',
            },
            {
                // Gate: the title of the target action, not ".o_list_view"
                // alone (patterns-navigation-and-form.md §A).
                content: "CoA and Mapping list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(CoA and Mapping)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // Flow 2 - Open the Open record. The client name is unique to
            // the fixture.
            {
                content: "Open the Open record",
                trigger:
                    ".o_list_view .o_data_row:contains(Test Audit Client - Import Account Tour) " +
                    ".o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // Flow 3 - On the Account Mappings tab, click Import Accounts
            {
                content: "Open the Account Mappings tab",
                trigger: ".o_notebook .nav-link:contains(Account Mappings)",
                extra_trigger: ".o_form_view",
            },
            {
                // Matched by its text: the view class oe_highlight is not
                // kept in the 14.0 DOM.
                content: "Click the Import Accounts button",
                trigger:
                    ".o_form_view .tab-pane.active button:contains(Import Accounts)",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 - The Import dialog is displayed (stop here: no upload)
            {
                content: "Import dialog is displayed",
                trigger: ".modal-title:contains(Import Client Account)",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            {
                content: "Dialog offers the File field",
                trigger: ".o_form_view [name='data']",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            {
                content: "Dialog offers the Import Preview field",
                trigger: ".o_form_view [name='import_summary']",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            {
                content: "Dialog offers the Import button",
                trigger: ".modal-footer button:contains(Import)",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            {
                content: "Close the dialog with Cancel",
                trigger: ".modal-footer button:contains(Cancel)",
            },

            // Post-Condition - dialog closed, record still Open
            {
                content: "Dialog is closed and status is Open",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='open'].btn-primary",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
