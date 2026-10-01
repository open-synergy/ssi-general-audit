/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html). */

odoo.define("ssi_general_audit.client_adjusting_coa_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Flow 1 of every tour below: open Risk Responses > Result > Adjusting
    // CoA. "Result" is a level-2 section (clickable) and "Adjusting CoA" its
    // leaf, so the tour needs one step per level -- see
    // odoo-development-ui-test-skill patterns-navigation-and-form.md §A.
    var openMenu = [
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
            content: "Open the Adjusting CoA menu",
            trigger:
                '.o_menu_sections [data-menu-xmlid="ssi_general_audit.adjusting_coa_menu"]',
        },
        {
            // Gate: the title of the target action. ".o_list_view" alone
            // would also match the app's landing list (patterns-navigation-
            // and-form.md §A).
            content: "Adjusting CoA list is displayed",
            trigger: ".o_control_panel .breadcrumb-item.active:contains(Adjusting CoA)",
            extra_trigger: ".o_list_view",
            run: function () {
                // Assertion only; do not trigger the default click action.
            },
        },
    ];

    // IK: docs/client_adjusting_coa/01-create.md
    tour.register(
        "ssi_general_audit_client_adjusting_coa_create",
        {
            test: true,
            url: "/web",
        },
        openMenu.concat([
            // Flow 2 - Click the New button ("Create" in 14.0)
            {
                content: "Click Create",
                trigger: ".o_list_button_add",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open in edit mode",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // Flow 3 - Fill in the # General Audit field
            {
                content: "Select the General Audit",
                trigger: ".o_field_many2one[name='general_audit_id'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-ACOA-GA",
            },
            {
                content: "Pick the General Audit from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR-ACOA-GA)",
            },

            // Flow 4 - Add one line on the Details tab
            {
                content: "Open the Details tab",
                trigger: ".o_notebook .nav-link:contains(Details)",
                extra_trigger: ".o_form_view.o_form_editable",
            },
            {
                content: "Add a line",
                trigger: ".o_field_x2many .o_field_x2many_list_row_add a",
                extra_trigger: ".o_form_view.o_form_editable",
            },
            {
                content: "Fill in the Code",
                trigger: ".o_selected_row .o_field_widget[name='code']",
                run: "text TOUR-ACOA-001",
            },
            {
                content: "Fill in the Name",
                trigger: ".o_selected_row .o_field_widget[name='name']",
                run: "text Tour New Account",
            },
            {
                // The Type field is filled last: it is the only many2one of
                // the row, so no onchange competes with its dropdown.
                content: "Select the Type",
                trigger: ".o_selected_row .o_field_many2one[name='type_id'] input",
                run: "text TOUR-ACOA-TYPE",
            },
            {
                content: "Pick the Type from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR-ACOA-TYPE)",
            },

            // Flow 5 - Click Save
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // Post-Condition - the record is in Draft status with its line.
            {
                content: "Status is Draft",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            {
                content: "The line is listed on the Details tab",
                trigger:
                    ".o_field_widget[name='detail_ids'] " +
                    ".o_data_row:contains(TOUR-ACOA-001)",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ])
    );

    // IK: docs/client_adjusting_coa/04-confirm.md
    tour.register(
        "ssi_general_audit_client_adjusting_coa_confirm",
        {
            test: true,
            url: "/web",
        },
        openMenu.concat([
            // Flow 2 - Open the record to confirm. The Draft record is the
            // only row whose state reads "Draft" (the other fixture waits
            // for approval).
            {
                content: "Open the Draft record",
                trigger: ".o_list_view .o_data_row:contains(Draft) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // Flow 3 - Click the Confirm button
            {
                content: "Click the Confirm button",
                trigger: ".o_statusbar_buttons button[name='action_confirm']",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 - Click OK on the confirmation dialog
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition - status changes to Waiting for Approval.
            {
                content: "Status is Waiting for Approval",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ])
    );

    // IK: docs/client_adjusting_coa/05-approve.md
    tour.register(
        "ssi_general_audit_client_adjusting_coa_approve",
        {
            test: true,
            url: "/web",
        },
        openMenu.concat([
            // Flow 2 - Open the record to approve.
            {
                content: "Open the record waiting for approval",
                trigger:
                    ".o_list_view .o_data_row:contains(Waiting for Approval) " +
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

            // Flow 3 - Click the Approve button
            {
                content: "Click the Approve button",
                trigger: ".o_statusbar_buttons button[name='action_approve_approval']",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 - Click OK on the confirmation dialog
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition - status changes to Done, and the account
            // created for the line is shown on the Details tab.
            {
                content: "Status is Done",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='done'].btn-primary",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            {
                content: "The account created for the line is shown",
                trigger:
                    ".o_field_widget[name='detail_ids'] " +
                    ".o_data_row:contains(TOUR-ACOA-C1)",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ])
    );
});
