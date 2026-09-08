/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html). */

odoo.define(
    "ssi_general_audit_worksheet_draft_reporting.general_audit_ws_ff42fdc_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/general_audit_ws_ff42fdc/01-load_posture.md
        tour.register(
            "ssi_general_audit_worksheet_draft_reporting_ff42fdc_load_posture",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 - Open the Windup & Reporting > Draft Reporting >
                // Final Discussion > Audit Result menu. "Final Discussion"
                // (level 3, has children) and "Audit Result Formulation"
                // section renders both are unclickable dropdown-headers
                // without data-menu-xmlid, so only the app, the "Draft
                // Reporting" section, and the "Audit Result" leaf get a
                // step -- see odoo-development-ui-test-skill
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
                    content: "Open the Audit Result menu",
                    trigger:
                        ".o_menu_sections " +
                        "[data-menu-xmlid='ssi_general_audit_worksheet_draft_reporting" +
                        ".general_audit_ws_ff42fdc_menu']",
                },
                {
                    // Gate: the app's landing action is "Audit Result
                    // Formulation" (lowest sequence under the app), and our
                    // target title "Audit Result" is a SUBSTRING of it, so a
                    // positive :contains() gate would match the stale
                    // landing page too. Wait for the landing title to be
                    // GONE instead -- see patterns-navigation-and-form.md
                    // §A "Cek tabrakan substring".
                    content: "Audit Result list is displayed",
                    trigger:
                        ".o_control_panel:not(:has(" +
                        ".breadcrumb-item.active:contains(Audit Result Formulation)))",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 2 - Open the worksheet to load the posture for
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

                // Flow 3 - Open the Posture Report tab
                {
                    content: "Open the Posture Report tab",
                    trigger: ".o_notebook .nav-link:contains(Posture Report)",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 - Click the Load Posture button
                {
                    content: "Click the Load Posture button",
                    trigger: ".tab-pane.active button[name='action_load_posture']",
                    extra_trigger: ".o_form_view",
                },

                // Post-Condition - the Posture Report table is (re)built.
                // No posture line exists before Load Posture is clicked (the
                // table starts empty), so a row naming the account group
                // fixture created in setUpClass can only appear AFTER the
                // click -- see patterns-advanced-gotchas.md §P.
                {
                    content: "Posture Report table shows the loaded row",
                    trigger:
                        ".o_field_widget[name='posture_ids'] " +
                        ".o_data_row:contains(TOUR-FF42FDC-GROUP)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );
    }
);
