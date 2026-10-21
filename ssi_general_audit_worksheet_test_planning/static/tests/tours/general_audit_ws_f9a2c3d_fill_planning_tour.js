/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html). */

odoo.define(
    "ssi_general_audit_worksheet_test_planning.general_audit_ws_f9a2c3d_fill_planning_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/general_audit_ws_f9a2c3d/02-isi-perencanaan.md
        tour.register(
            "ssi_general_audit_worksheet_test_planning_f9a2c3d_fill_planning",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 - Open the Risk Responses > Substantive Test >
                // Test of Detail Planning menu.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Risk Responses app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_general_audit.menu_risk_responses_root"]',
                },
                {
                    content: "Open the Substantive Test menu",
                    trigger:
                        ".o_menu_sections " +
                        '[data-menu-xmlid="ssi_general_audit.menu_rr_substantive_test"]',
                },
                {
                    content: "Open the Test of Detail Planning menu",
                    trigger:
                        ".o_menu_sections " +
                        "[data-menu-xmlid='ssi_general_audit_worksheet_test_planning" +
                        ".general_audit_ws_f9a2c3d_menu']",
                },
                {
                    content: "Test of Detail Planning list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(" +
                        "Test of Detail Planning)",
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
                    content: "Open the Details tab",
                    trigger: ".o_notebook .nav-link:contains(Details)",
                    extra_trigger: ".o_form_view",
                },

                // Flow 3 - Click Edit. The worksheet form is read-only until
                // then, and a click on a row of the Details list would open a
                // read-only row dialog instead of editing the row in place.
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

                // Flow 4 - Click the Timing cell of the account line.
                // Cell 7 of the Details list: Standard Account(0), Account
                // Type(1), Balance(2), Performance Materiality(3), ROMM(4),
                // Assersion Types(5), AP Result(6), Timing(7), Extent(8),
                // Primary Audit Technique(9). The currency column is
                // invisible and renders no cell.
                {
                    content: "Click the Timing cell of the account line",
                    trigger:
                        ".tab-pane.active .o_field_widget[name='detail_ids'] " +
                        ".o_data_row:contains(TOUR-F9A2C3D-TYPE) .o_data_cell:eq(7)",
                    extra_trigger: ".o_form_view",
                },
                {
                    content: "Type the timing",
                    trigger: ".o_selected_row .o_field_widget[name='timing_id'] input",
                    run: "text Interim",
                },
                {
                    content: "Choose Interim Testing",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(Interim Testing)",
                },

                // Flow 5 - Extent.
                {
                    content: "Type the extent",
                    trigger: ".o_selected_row .o_field_widget[name='extent_id'] input",
                    run: "text Sampling",
                },
                {
                    content: "Choose Sampling",
                    trigger: ".ui-autocomplete .ui-menu-item a:contains(Sampling)",
                },

                // Flow 6 - Primary Audit Technique, two values.
                {
                    content: "Type the first technique",
                    trigger:
                        ".o_selected_row .o_field_widget[name='technique_ids'] input",
                    run: "text Inspection",
                },
                {
                    content: "Choose Inspection",
                    trigger: ".ui-autocomplete .ui-menu-item a:contains(Inspection)",
                },
                {
                    content: "Type the second technique",
                    trigger:
                        ".o_selected_row .o_field_widget[name='technique_ids'] input",
                    // Wait until the first tag is rendered, the input is
                    // re-created after each choice.
                    extra_trigger:
                        ".o_selected_row .o_field_widget[name='technique_ids'] " +
                        ".o_badge_text:contains(Inspection)",
                    run: "text Observation",
                },
                {
                    content: "Choose Observation",
                    trigger: ".ui-autocomplete .ui-menu-item a:contains(Observation)",
                },

                // Flow 7 - Save. The last cell is committed by selecting
                // another cell of the same line first (the Account Type
                // cell, which is read-only) -- see patterns-fields.md §C
                // "Jebakan 2".
                {
                    content: "Commit the technique by selecting another cell",
                    trigger: ".o_selected_row .o_data_cell:eq(1)",
                    run: "click",
                },
                {
                    content: "Click Save",
                    trigger: ".o_form_button_save",
                    extra_trigger: ".o_form_view.o_form_editable",
                },

                // Post-Condition - the line shows the chosen values as text.
                // While the row was in edit mode the values were input values,
                // not text, so these rows can only match AFTER the save.
                {
                    content: "The line shows the timing",
                    trigger:
                        ".o_field_widget[name='detail_ids'] " +
                        ".o_data_row:contains(Interim Testing)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "The line shows the extent",
                    trigger:
                        ".o_field_widget[name='detail_ids'] " +
                        ".o_data_row:contains(Sampling)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "The line shows the first technique",
                    trigger:
                        ".o_field_widget[name='detail_ids'] " +
                        ".o_data_row .o_badge_text:contains(Inspection)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "The line shows the second technique",
                    trigger:
                        ".o_field_widget[name='detail_ids'] " +
                        ".o_data_row .o_badge_text:contains(Observation)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );
    }
);
