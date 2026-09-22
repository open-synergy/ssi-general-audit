/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html). */

odoo.define(
    "ssi_general_audit_worksheet_final_report.general_audit_ws_b66777d_team_allocation_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/general_audit_ws_b66777d/02-view-final-team-allocation.md
        tour.register(
            "ssi_general_audit_worksheet_final_report_b66777d_view_final_team_allocation",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 - Open the Windup & Reporting > Final Report >
                // Independen Auditor Report menu.
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
                    content: "Open the Independen Auditor Report menu",
                    trigger:
                        ".o_menu_sections " +
                        "[data-menu-xmlid='ssi_general_audit_worksheet_final_report" +
                        ".general_audit_ws_b66777d_menu']",
                },
                {
                    content: "Independen Auditor Report list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active" +
                        ":contains(Independen Auditor Report)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 2 - Open the worksheet to view the final team
                // allocations for
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

                // Flow 3 - Open the Final Team Allocations tab
                {
                    content: "Open the Final Team Allocations tab",
                    trigger: ".o_notebook .nav-link:contains(Final Team Allocations)",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 - Click Populate. Object-type button that writes
                // team_allocation_ids asynchronously, so the next step's
                // trigger must name something that only exists AFTER the
                // write lands -- here, a data row for the fixture's team
                // member, which the table does not contain before
                // Populate is clicked. See odoo-development-ui-test skill
                // patterns-advanced-gotchas.md §P.
                {
                    content: "Click the Populate button",
                    trigger:
                        ".o_form_view button[name='action_populate_team_allocation']",
                    extra_trigger: ".o_form_view",
                },
                {
                    content: "A row for the fixture's team member appears",
                    trigger:
                        ".tab-pane.active " +
                        ".o_field_widget[name='team_allocation_ids'] " +
                        ".o_data_row:contains(Team Allocation Tour Employee)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );
    }
);
