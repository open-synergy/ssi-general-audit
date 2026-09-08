/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html). */

odoo.define(
    "ssi_general_audit_worksheet_draft_reporting.general_audit_ws_de69c2f_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/general_audit_ws_de69c2f/02-reload_audit_result.md
        tour.register(
            "ssi_general_audit_worksheet_draft_reporting_de69c2f_reload_audit_result",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 - Open the Windup & Reporting > Draft Reporting >
                // Final Discussion menu. "Final Discussion" (level 3, has
                // children) and the section header render as unclickable
                // dropdown-headers without data-menu-xmlid, so only the
                // app, the "Draft Reporting" section, and the "Final
                // Discussion" leaf get a step -- see
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
                    content: "Open the Final Discussion menu",
                    trigger:
                        ".o_menu_sections " +
                        "[data-menu-xmlid='ssi_general_audit_worksheet_draft_reporting" +
                        ".general_audit_ws_de69c2f_menu']",
                },
                {
                    content: "Final Discussion list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Final Discussion)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 2 - Open the worksheet to reload the Audit Result
                // reference for
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

                // Flow 3 - Open the Audit Result tab
                {
                    content: "Open the Audit Result tab",
                    trigger: ".o_notebook .nav-link:contains(Audit Result)",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 - Click the Reload button
                {
                    content: "Click the Reload button",
                    trigger:
                        ".tab-pane.active button[name='action_reload_audit_result']",
                    extra_trigger: ".o_form_view",
                },

                // Post-Condition - the # Audit Result field shows the
                // document number of the ff42fdc sibling. audit_result_id
                // is readonly=True and empty before Reload is clicked
                // (setUpClass creates the sibling but never calls the
                // reload): a readonly m2o field with no value renders as
                // a zero-pixel <span> (no text), so this trigger cannot
                // match until Reload actually fills it -- see
                // patterns-advanced-gotchas.md §P "Field readonly tanpa
                // nilai = kotak nol piksel".
                {
                    content: "Audit Result field is filled",
                    trigger: ".tab-pane.active .o_field_widget[name='audit_result_id']",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );

        // IK: docs/general_audit_ws_de69c2f/03-reload_management_letter.md
        tour.register(
            "ssi_general_audit_worksheet_draft_reporting_de69c2f_reload_management_letter",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 - Open the Windup & Reporting > Draft Reporting >
                // Final Discussion menu
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
                    content: "Open the Final Discussion menu",
                    trigger:
                        ".o_menu_sections " +
                        "[data-menu-xmlid='ssi_general_audit_worksheet_draft_reporting" +
                        ".general_audit_ws_de69c2f_menu']",
                },
                {
                    content: "Final Discussion list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Final Discussion)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 2 - Open the worksheet to reload the Management
                // Letter reference for
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

                // Flow 3 - Open the Management Letter tab
                {
                    content: "Open the Management Letter tab",
                    trigger: ".o_notebook .nav-link:contains(Management Letter)",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 - Click the Reload button
                {
                    content: "Click the Reload button",
                    trigger:
                        ".tab-pane.active button[name='action_reload_management_letter']",
                    extra_trigger: ".o_form_view",
                },

                // Post-Condition - the # Management Letter field shows the
                // document number of the ae598e6 sibling.
                // management_letter_id is readonly=True and empty before
                // Reload is clicked, so this trigger cannot match until
                // Reload fills it -- see patterns-advanced-gotchas.md §P
                // "Field readonly tanpa nilai = kotak nol piksel".
                {
                    content: "Management Letter field is filled",
                    trigger:
                        ".tab-pane.active .o_field_widget[name='management_letter_id']",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );

        // IK: docs/general_audit_ws_de69c2f/04-reload_management_representation.md
        tour.register(
            "ssi_general_audit_worksheet_draft_reporting_de69c2f_reload_management_representation",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 - Open the Windup & Reporting > Draft Reporting >
                // Final Discussion menu
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
                    content: "Open the Final Discussion menu",
                    trigger:
                        ".o_menu_sections " +
                        "[data-menu-xmlid='ssi_general_audit_worksheet_draft_reporting" +
                        ".general_audit_ws_de69c2f_menu']",
                },
                {
                    content: "Final Discussion list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Final Discussion)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 2 - Open the worksheet to reload the Management
                // Representation reference for
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

                // Flow 3 - Open the Management Representation tab
                {
                    content: "Open the Management Representation tab",
                    trigger:
                        ".o_notebook .nav-link:contains(Management Representation)",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 - Click the Reload button
                {
                    content: "Click the Reload button",
                    trigger:
                        ".tab-pane.active " +
                        "button[name='action_reload_management_representation']",
                    extra_trigger: ".o_form_view",
                },

                // Post-Condition - the # Management Representation field
                // shows the document number of the bbbdfe7 sibling.
                // management_representation_id is readonly=True and empty
                // before Reload is clicked, so this trigger cannot match
                // until Reload fills it -- see
                // patterns-advanced-gotchas.md §P "Field readonly tanpa
                // nilai = kotak nol piksel".
                {
                    content: "Management Representation field is filled",
                    trigger:
                        ".tab-pane.active " +
                        ".o_field_widget[name='management_representation_id']",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );
    }
);
