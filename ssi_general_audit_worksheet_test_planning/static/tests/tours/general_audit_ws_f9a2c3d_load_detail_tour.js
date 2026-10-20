/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html). */

odoo.define(
    "ssi_general_audit_worksheet_test_planning.general_audit_ws_f9a2c3d_load_detail_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/general_audit_ws_f9a2c3d/01-load-detail.md
        tour.register(
            "ssi_general_audit_worksheet_test_planning_f9a2c3d_load_detail",
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

                // Flow 2 - Open the worksheet to load the lines for.
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

                // Flow 3 - Open the Details tab (the first tab).
                {
                    content: "Open the Details tab",
                    trigger: ".o_notebook .nav-link:contains(Details)",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 - Click the Detail button.
                {
                    content: "Click the Detail button",
                    trigger: ".tab-pane.active button[name='action_load_detail']",
                    extra_trigger: ".o_form_view",
                },

                // Post-Condition - one line per standard account. The table
                // starts empty (no line is loaded in setUpClass), so a row
                // naming the account type fixture can only appear AFTER the
                // click -- see patterns-advanced-gotchas.md §P.
                {
                    content: "Details table shows the loaded account",
                    trigger:
                        ".o_field_widget[name='detail_ids'] " +
                        ".o_data_row:contains(TOUR-F9A2C3D-TYPE)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Details table shows the Balance column",
                    trigger: ".o_field_widget[name='detail_ids'] th:contains(Balance)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Details table shows the Performance Materiality column",
                    trigger:
                        ".o_field_widget[name='detail_ids'] " +
                        "th:contains(Performance Materiality)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Details table shows the AP Result column",
                    trigger:
                        ".o_field_widget[name='detail_ids'] th:contains(AP Result)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Details table shows the Timing column",
                    trigger: ".o_field_widget[name='detail_ids'] th:contains(Timing)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Details table shows the Extent column",
                    trigger: ".o_field_widget[name='detail_ids'] th:contains(Extent)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Details table shows the Primary Audit Technique column",
                    trigger:
                        ".o_field_widget[name='detail_ids'] " +
                        "th:contains(Primary Audit Technique)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );
    }
);
