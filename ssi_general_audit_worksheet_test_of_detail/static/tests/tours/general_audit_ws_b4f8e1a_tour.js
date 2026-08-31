/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html). */

odoo.define(
    "ssi_general_audit_worksheet_test_of_detail.general_audit_ws_b4f8e1a_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/general_audit_ws_b4f8e1a/01-isi-data-dan-generate.md
        tour.register(
            "ssi_general_audit_worksheet_test_of_detail_b4f8e1a_generate_examination_data",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 - Open the Risk Responses > Result > Test of Detail menu
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
                    content: "Open the Test of Detail menu",
                    trigger:
                        ".o_menu_sections " +
                        "[data-menu-xmlid='ssi_general_audit_worksheet_test_of_detail" +
                        ".general_audit_ws_b4f8e1a_menu']",
                },
                {
                    // Gate: wait for the TARGET action, not just any list view --
                    // clicking Result lands on its first sub-menu first.
                    content: "Test of Detail list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Test of Detail)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 2 - Open the worksheet to fill in
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

                // Flow 3 - Select the Data Mode: General Ledger
                {
                    content: "Select Data Mode = General Ledger",
                    trigger: "select.o_field_widget[name='data_mode']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text General Ledger",
                },

                // Flow 4 - Select the matching General Ledger record
                {
                    content: "Open the General Ledger dropdown",
                    trigger: ".o_field_many2one[name='general_ledger_id'] input",
                    run: "click",
                },
                {
                    content: "Pick the only allowed General Ledger from the dropdown",
                    trigger:
                        ".ui-autocomplete:visible " +
                        ".ui-menu-item:not(.o_m2o_start_typing) a:eq(0)",
                    in_modal: false,
                },

                // Flow 5 - Select the Data Source: Population
                {
                    content: "Select Data Source = Population",
                    trigger: "select.o_field_widget[name='data_source']",
                    run: "text Population",
                },

                // Flow 6 - Fill in the Identifier Column Number (Population branch)
                {
                    content: "Fill in Identifier Column Number",
                    trigger: ".o_field_widget[name='identifier_col_number']",
                    run: "text 1",
                },

                // Flow 7 - Click the Generate Examination Data button
                {
                    content: "Click the Generate Examination Data button",
                    trigger: "button[name='action_generate_examination_data']",
                    extra_trigger: ".o_form_view",
                },

                // Post-Condition - the Examination Data table is (re)built from
                // the General Ledger's Raw Data. The gate below can only ever
                // match AFTER Generate is clicked: the worksheet is freshly
                // opened with no Examination Data yet, and the identifier value
                // asserted here only exists in the General Ledger's Raw Data,
                // not anywhere else on the form.
                {
                    content: "Examination Data table shows the generated row",
                    trigger:
                        ".o_field_widget[name='examination_data'] " +
                        "input.csv_table_cell_input[value='TOUR-B4F8E1A-R1']",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );
    }
);
