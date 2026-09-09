/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html). */

odoo.define(
    "ssi_general_audit_worksheet_draft_reporting.general_audit_ws_de69c2f_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/general_audit_ws_de69c2f/02-reload_links.md
        tour.register(
            "ssi_general_audit_worksheet_draft_reporting_de69c2f_reload_links",
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

                // Flow 2 - Open the worksheet to view/refresh the Links tab for
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

                // Flow 3 - Open the Links tab
                {
                    content: "Open the Links tab",
                    trigger: ".o_notebook .nav-link:contains(Links)",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 - Click the Reload button. Unlike the per-KKA
                // Reload buttons of the previous design, this one sits
                // BEFORE <notebook> (form level, not inside a tab-pane) --
                // see general_audit_ws_fbbe0f8_views.xml for the pattern
                // this worksheet mirrors.
                {
                    content: "Click the Reload button",
                    trigger: ".o_form_view button[name='action_reload_links']",
                    extra_trigger: ".o_form_view",
                },

                // Post-Condition - the Links tab shows the Audit Result
                // reference. audit_result_id is a compute+store field
                // (implicitly readonly, force_save="1") and is still empty
                // when the tour opens the worksheet -- setUpClass creates
                // the de69c2f worksheet BEFORE its ff42fdc sibling exists,
                // so the initial compute finds nothing and the sibling
                // created afterwards never retriggers it. A readonly m2o
                // field with no value renders as a zero-pixel <span> (no
                // text), so this trigger cannot match until Reload actually
                // fills it -- see patterns-advanced-gotchas.md §P "Field
                // readonly tanpa nilai = kotak nol piksel".
                {
                    content: "Audit Result field is filled",
                    trigger: ".tab-pane.active .o_field_widget[name='audit_result_id']",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );
    }
);
