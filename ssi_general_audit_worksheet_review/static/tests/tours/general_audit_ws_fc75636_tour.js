/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html). */

odoo.define(
    "ssi_general_audit_worksheet_review.general_audit_ws_fc75636_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/general_audit_ws_fc75636/01-reload_links.md
        tour.register(
            "ssi_general_audit_worksheet_review_fc75636_reload_links",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 - Open the Windup & Reporting > Final Report >
                // Proposed Audit Opinion menu.
                //
                // "Final Report" (level 2) has children (Audit Final
                // Memorandum, Proposed Audit Opinion, ...), so it renders
                // as a clickable dropdown-toggle section. "Proposed Audit
                // Opinion" (level 3, general_audit_ws_fc75636_menu) has
                // no children of its own, so it is a clickable leaf
                // directly inside the "Final Report" dropdown -- see
                // odoo-development-ui-test skill
                // references/patterns-navigation-and-form.md §A.
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
                    content: "Open the Proposed Audit Opinion menu",
                    trigger:
                        ".o_menu_sections " +
                        "[data-menu-xmlid='ssi_general_audit_worksheet_review" +
                        ".general_audit_ws_fc75636_menu']",
                },
                {
                    content: "Proposed Audit Opinion list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active" +
                        ":contains(Proposed Audit Opinion)",
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

                // Flow 4 - Click the Reload button
                {
                    content: "Click the Reload button",
                    trigger: ".o_form_view button[name='action_reload_links']",
                    extra_trigger: ".o_form_view",
                },

                // Post-Condition - the Links tab shows the Audit Final
                // Memorandum reference. audit_final_memorandum_id is a
                // compute+store field (implicitly readonly,
                // force_save="1") and is still empty when the tour opens
                // the worksheet -- setUpClass creates the fc75636
                // worksheet BEFORE its a8c54f3 sibling is opened, so the
                // initial compute finds nothing and the sibling opened
                // afterwards never retriggers it. A readonly m2o field
                // with no value renders as a zero-pixel <span> (no text),
                // so this trigger cannot match until Reload actually
                // fills it -- see patterns-advanced-gotchas.md §P "Field
                // readonly tanpa nilai = kotak nol piksel".
                {
                    content: "Audit Final Memorandum field is filled",
                    trigger:
                        ".tab-pane.active " +
                        ".o_field_widget[name='audit_final_memorandum_id']",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Proposed Audit Opinion field is filled",
                    trigger:
                        ".tab-pane.active " +
                        ".o_field_widget[name='proposed_audit_opinion_id']",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );
    }
);
