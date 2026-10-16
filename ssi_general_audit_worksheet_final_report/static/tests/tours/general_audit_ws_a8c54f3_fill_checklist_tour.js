/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html). */

odoo.define(
    "ssi_general_audit_worksheet_final_report.general_audit_ws_a8c54f3_fill_checklist_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/general_audit_ws_a8c54f3/01-fill-checklist.md
        tour.register(
            "ssi_general_audit_worksheet_final_report_a8c54f3_fill_checklist",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 - Open the Windup & Reporting > Final Report >
                // Audit Final Memorandum menu.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Windup & Reporting app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_general_audit.menu_wind_up_reporting_root"]',
                },
                {
                    content: "Open the Final Report menu",
                    trigger:
                        ".o_menu_sections " +
                        '[data-menu-xmlid="ssi_general_audit.menu_general_audit_final_report"]',
                },
                {
                    content: "Open the Audit Final Memorandum menu",
                    trigger:
                        ".o_menu_sections " +
                        "[data-menu-xmlid='ssi_general_audit_worksheet_final_report" +
                        ".general_audit_ws_a8c54f3_menu']",
                },
                {
                    content: "Audit Final Memorandum list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active" +
                        ":contains(Audit Final Memorandum)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 2 - Open the worksheet.
                {
                    content: "Open the worksheet",
                    trigger: ".o_list_view .o_data_row:first .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Worksheet form is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 3 - Open the Checklist tab, the first tab (left of Links).
                {
                    content: "The Checklist tab is the first tab",
                    trigger:
                        ".o_notebook .nav-item:first-child .nav-link:contains(Checklist)",
                    extra_trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Open the Checklist tab",
                    trigger: ".o_notebook .nav-link:contains(Checklist)",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 - Click Populate. Object-type button that writes
                // checklist_ids asynchronously, so the next step names a
                // row that does not exist before Populate is clicked.
                {
                    content: "Click the Populate button",
                    trigger: ".o_form_view button[name='action_populate_checklist']",
                    extra_trigger: ".o_form_view",
                },
                {
                    content: "The first checklist item appears",
                    trigger:
                        ".tab-pane.active " +
                        ".o_field_widget[name='checklist_ids'] " +
                        ".o_data_row:contains(Client legal name)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 5 - Click Edit. 14.0: an opened existing record is
                // READONLY, and Populate (type=object) does not make it
                // editable, so the row dialog would be readonly too.
                {
                    content: "Click the Edit button",
                    trigger: ".o_form_button_edit",
                },
                {
                    content: "Form is now editable",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 6 - Open the row and choose the Option.
                {
                    content: "Open the first checklist row",
                    trigger:
                        ".tab-pane.active " +
                        ".o_field_widget[name='checklist_ids'] " +
                        ".o_data_row:contains(Client legal name) .o_data_cell:first",
                },
                {
                    content: "Fill the Option field with Yes",
                    trigger: ".o_field_many2one[name='option_id'] input",
                    run: "text Yes",
                },
                {
                    content: "Pick Yes from the dropdown",
                    trigger: ".ui-autocomplete:visible li a:contains(Yes)",
                    in_modal: false,
                },

                // Flow 7 - Save & Close.
                {
                    content: "Click Save & Close",
                    trigger: ".modal-footer button.btn-primary",
                },
                {
                    content: "The row shows the chosen Option",
                    trigger:
                        "body:not(:has(.modal)) .tab-pane.active " +
                        ".o_field_widget[name='checklist_ids'] " +
                        ".o_data_row:contains(Client legal name):contains(Yes)",
                    in_modal: false,
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 8 - Save.
                {
                    content: "Click Save",
                    trigger: ".o_form_button_save",
                    in_modal: false,
                },
                {
                    content: "The form is back in read mode",
                    trigger: ".o_form_view.o_form_readonly",
                    in_modal: false,
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );
    }
);
