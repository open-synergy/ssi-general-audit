/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html). */

odoo.define("ssi_general_audit.client_adjustment_entry_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/client_adjustment_entry/01-import.md
    //
    // Flow 4-6 (select the CSV file, click Import, check the new lines)
    // are NOT driven by this tour: the file upload dialog of the browser
    // has no DOM completion signal and can hang headless Chrome. The tour
    // proves the Import button opens the wizard, then closes it with
    // Cancel. The imported values are covered by the unit tests in
    // tests/test_import_adjustment_entry_detail.py.
    tour.register(
        "ssi_general_audit_client_adjustment_entry_import",
        {
            test: true,
            url: "/web",
        },
        [
            // Flow 1 - Open Risk Responses > Result > Adjusting Journal
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Risk Responses app",
                trigger:
                    '.o_app[data-menu-xmlid="ssi_general_audit.menu_risk_responses_root"]',
            },
            {
                content: "Open the Result menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_general_audit.menu_rr_result"]',
            },
            {
                content: "Open the Adjusting Journal menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_general_audit.adjustment_entry_menu"]',
            },
            {
                // Gate: the title of the target action, not ".o_list_view"
                // alone (patterns-navigation-and-form.md §A).
                content: "Adjusting Journal list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Adjusting Journal)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // Flow 2 - Open the Draft record. The client name is unique
            // to the fixture.
            {
                content: "Open the Draft record",
                trigger:
                    ".o_list_view .o_data_row:contains(Test Audit Client - Adjustment Entry Tour) " +
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

            // Flow 3 - On the Details tab, click the Import button
            {
                content: "Open the Details tab",
                trigger: ".o_notebook .nav-link:contains(Details)",
                extra_trigger: ".o_form_view",
            },
            {
                content: "Click the Import button",
                trigger:
                    ".o_form_view .tab-pane.active button.oe_highlight:contains(Import)",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 - The Import dialog is displayed (stop here: no upload)
            {
                content: "Import dialog is displayed",
                trigger: ".modal-title:contains(Import Adjustment Entry Detail)",
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
                content: "Close the dialog with Cancel",
                trigger: ".modal-footer button:contains(Cancel)",
            },

            // Post-Condition - dialog closed, record still Draft
            {
                content: "Dialog is closed and status is Draft",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
