/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html). */

odoo.define(
    "ssi_general_audit_worksheet_draft_reporting.general_audit_ws_b555edd_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/general_audit_ws_b555edd/01-create.md
        tour.register(
            "ssi_general_audit_worksheet_draft_reporting_b555edd_create",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 - Open the Windup & Reporting > Draft Reporting >
                // Report Formatting Control menu. "Draft Reporting" (has
                // children) renders as a dropdown section; the leaf below
                // it has data-menu-xmlid and is directly clickable -- see
                // odoo-development-ui-test-skill
                // patterns-navigation-and-form.md §A.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Windup & Reporting app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_general_audit.menu_wind_up_reporting_root"]',
                },
                {
                    content: "Open the Draft Reporting menu",
                    trigger:
                        ".o_menu_sections " +
                        '[data-menu-xmlid="ssi_general_audit.menu_general_audit_draft_reporting"]',
                },
                {
                    content: "Open the Report Formatting Control menu",
                    trigger:
                        ".o_menu_sections " +
                        "[data-menu-xmlid='ssi_general_audit_worksheet_draft_reporting" +
                        ".general_audit_ws_b555edd_menu']",
                },
                {
                    content: "Report Formatting Control list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Report Formatting Control)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 2 - Click the Create button. (14.0 label: "Create")
                {
                    content: "Click the Create button",
                    trigger: ".o_list_button_add",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "A new record form is open",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 3 - Fill in the required General Audit field.
                {
                    content: "Select the General Audit",
                    trigger: ".o_field_many2one[name='general_audit_id'] input",
                    run: "text Test General Audit - B555EDD Tour",
                },
                {
                    // The "Create" quick-create option is rendered as
                    // Create "<strong>Test General Audit - B555EDD
                    // Tour</strong>" -- its text also contains the typed
                    // string, so :contains() alone matches it too (CI
                    // screenshot confirmed the tour landed on a blank
                    // "Create: General Audit" dialog instead of picking
                    // the fixture). Both "Create" and "Create and Edit..."
                    // options carry the o_m2o_dropdown_option class
                    // (odoo/addons/web/static/src/js/fields/
                    // relational_fields.js), which real record matches do
                    // not -- exclude it.
                    content: "Pick the General Audit from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item " +
                        "a:contains(Test General Audit - B555EDD Tour):not(.o_m2o_dropdown_option)",
                    in_modal: false,
                },

                // Flow 4 - Save. accountant_id/partner_id/title are
                // auto-filled by the general_audit_id onchange, but
                // accountant_id renders as an editable many2one INPUT
                // here (not readonly text), so its value lives in the
                // input's `value` attribute, not as DOM text content --
                // :contains() never matches an attribute (CI log
                // confirmed the field genuinely is `<input
                // name="accountant_id">`). Asserting the specific
                // auto-filled value is unit-test territory anyway ("Tour
                // TIDAK menguji nilai"); the worksheet's own
                // accountant_id ends up correct because it is `related`
                // to general_audit_id, which IS asserted below.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // Post-Condition - a new record is created in Draft status.
                {
                    content: "Status is Draft",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Post-Condition - both statement tabs are visible on the
                // form, even though both are still empty at this point.
                {
                    content: "The Statement of Financial Position tab is visible",
                    trigger:
                        ".o_notebook .nav-link:contains(Statement of Financial Position)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "The Statement of Comprehensive Income tab is visible",
                    trigger:
                        ".o_notebook .nav-link:contains(Statement of Comprehensive Income)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );

        // IK: docs/general_audit_ws_b555edd/08-open.md
        tour.register(
            "ssi_general_audit_worksheet_draft_reporting_b555edd_open",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 - Open the Windup & Reporting > Draft Reporting >
                // Report Formatting Control menu.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Windup & Reporting app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_general_audit.menu_wind_up_reporting_root"]',
                },
                {
                    content: "Open the Draft Reporting menu",
                    trigger:
                        ".o_menu_sections " +
                        '[data-menu-xmlid="ssi_general_audit.menu_general_audit_draft_reporting"]',
                },
                {
                    content: "Open the Report Formatting Control menu",
                    trigger:
                        ".o_menu_sections " +
                        "[data-menu-xmlid='ssi_general_audit_worksheet_draft_reporting" +
                        ".general_audit_ws_b555edd_menu']",
                },

                // Flow 2 - Open the record to start. setUpClass leaves
                // exactly one Draft-state b555edd worksheet (worksheet_draft);
                // its state badge text is the only stable anchor since the
                // document number is still "/" before Start assigns one.
                {
                    content: "Open the draft worksheet",
                    trigger: ".o_data_row:contains(Draft) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Worksheet form is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 3 - Click the Start button.
                {
                    content: "Click the Start button",
                    trigger: ".o_statusbar_buttons button[name='action_open']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 - Click OK on the confirmation dialog
                // (action_open carries confirm="Start data. Are you sure?").
                // No ".modal" prefix -- 14.0, see patterns-dialogs-and-wizards.md §H.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Assertion - status is now On Progress (open). Gated on the
                // modal being closed -- §K.
                {
                    content: "Status is On Progress",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='open'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 5 - The Statement of Financial Position tab is the
                // first tab on the form; click its Reload button. The
                // button is only visible while the worksheet is Draft or
                // On Progress, so it also proves the status change above.
                {
                    content: "Open the Statement of Financial Position tab",
                    trigger:
                        ".o_notebook .nav-link:contains(Statement of Financial Position)",
                    extra_trigger: ".o_form_view",
                },
                {
                    content: "Click the Reload button",
                    trigger: ".tab-pane.active button[name='action_reload_account']",
                    extra_trigger: ".tab-pane.active",
                },
                {
                    content: "The statement lines table is displayed",
                    trigger: ".tab-pane.active .o_field_widget[name='sfp_detail_ids']",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 6 - Open the Statement of Comprehensive Income tab.
                {
                    content: "Open the Statement of Comprehensive Income tab",
                    trigger:
                        ".o_notebook .nav-link:contains(Statement of Comprehensive Income)",
                    extra_trigger: ".o_form_view",
                },
                {
                    content: "The comprehensive income lines table is displayed",
                    trigger: ".tab-pane.active .o_field_widget[name='soci_detail_ids']",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );

        // IK: docs/general_audit_ws_b555edd/04-confirm.md
        tour.register(
            "ssi_general_audit_worksheet_draft_reporting_b555edd_confirm",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 - Open the Windup & Reporting > Draft Reporting >
                // Report Formatting Control menu.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Windup & Reporting app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_general_audit.menu_wind_up_reporting_root"]',
                },
                {
                    content: "Open the Draft Reporting menu",
                    trigger:
                        ".o_menu_sections " +
                        '[data-menu-xmlid="ssi_general_audit.menu_general_audit_draft_reporting"]',
                },
                {
                    content: "Open the Report Formatting Control menu",
                    trigger:
                        ".o_menu_sections " +
                        "[data-menu-xmlid='ssi_general_audit_worksheet_draft_reporting" +
                        ".general_audit_ws_b555edd_menu']",
                },

                // Flow 2 - Open the record to confirm. setUpClass leaves
                // exactly one On Progress b555edd worksheet (worksheet_open).
                {
                    content: "Open the on-progress worksheet",
                    trigger: ".o_data_row:contains(On Progress) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Worksheet form is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 3 - Click the Confirm button. Conclusion is already
                // filled by the fixture (setUpClass) -- see
                // TestUiGeneralAuditWsE59c663.setUpClass docstring.
                {
                    content: "Click the Confirm button",
                    trigger: ".o_statusbar_buttons button[name='action_confirm']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 - Click OK on the confirmation dialog
                // (action_confirm carries confirm="Confirm data. Are you sure?").
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition - status is Waiting for Approval (confirm).
                {
                    content: "Status is Waiting for Approval",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Post-Condition - both statement tabs remain visible
                // after confirming.
                {
                    content: "The Statement of Financial Position tab is still visible",
                    trigger:
                        ".o_notebook .nav-link:contains(Statement of Financial Position)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content:
                        "The Statement of Comprehensive Income tab is still visible",
                    trigger:
                        ".o_notebook .nav-link:contains(Statement of Comprehensive Income)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );
    }
);
