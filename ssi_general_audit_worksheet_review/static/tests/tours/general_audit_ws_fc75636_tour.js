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

        // IK: docs/general_audit_ws_fc75636/02-fill-draft-opinion.md
        tour.register(
            "ssi_general_audit_worksheet_review_fc75636_fill_draft_opinion",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 - Open the Windup & Reporting > Final Report >
                // Proposed Audit Opinion menu.
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

                // Flow 2 - Open the worksheet to draft the audit opinion for
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

                // Flow 3 - Open the Draft Audit Opinion tab
                {
                    content: "Open the Draft Audit Opinion tab",
                    trigger: ".o_notebook .nav-link:contains(Draft Audit Opinion)",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 - Fill in the nine narrative fields
                {
                    content: "Fill in the Opinion field",
                    trigger:
                        ".tab-pane.active " +
                        ".o_field_widget[name='draft_opinion'] .note-editable",
                    run: "text Draft opinion narrative for this engagement.",
                },
                {
                    content: "Fill in the Basis for Opinion field",
                    trigger:
                        ".tab-pane.active " +
                        ".o_field_widget[name='draft_basis_for_opinion']" +
                        " .note-editable",
                    run: "text Draft basis for opinion narrative for this engagement.",
                },
                {
                    content: "Fill in the Key Audit Matters field",
                    trigger:
                        ".tab-pane.active " +
                        ".o_field_widget[name='draft_key_audit_matters']" +
                        " .note-editable",
                    run: "text Draft key audit matters narrative for this engagement.",
                },
                {
                    content: "Fill in the Other Information field",
                    trigger:
                        ".tab-pane.active " +
                        ".o_field_widget[name='draft_other_information']" +
                        " .note-editable",
                    run: "text Draft other information narrative for this engagement.",
                },
                {
                    content: "Fill in the Responsibilities of Management field",
                    trigger:
                        ".tab-pane.active " +
                        ".o_field_widget[name='draft_responsibilities_of_management']" +
                        " .note-editable",
                    run:
                        "text Draft responsibilities of management narrative for " +
                        "this engagement.",
                },
                {
                    content: "Fill in the Auditor's Responsibilities field",
                    trigger:
                        ".tab-pane.active " +
                        ".o_field_widget[name='draft_auditor_responsibilities']" +
                        " .note-editable",
                    run:
                        "text Draft auditor's responsibilities narrative for " +
                        "this engagement.",
                },
                {
                    content:
                        "Fill in the Report on Other Legal and Regulatory " +
                        "Requirements field",
                    trigger:
                        ".tab-pane.active " +
                        ".o_field_widget[name='draft_other_legal_regulatory']" +
                        " .note-editable",
                    run:
                        "text Draft other legal and regulatory requirements " +
                        "narrative for this engagement.",
                },
                {
                    content: "Fill in the Emphasis of Matter field",
                    trigger:
                        ".tab-pane.active " +
                        ".o_field_widget[name='draft_emphasis_of_matter']" +
                        " .note-editable",
                    run: "text Draft emphasis of matter narrative for this engagement.",
                },
                {
                    content: "Fill in the Other Matter field",
                    trigger:
                        ".tab-pane.active " +
                        ".o_field_widget[name='draft_other_matter']" +
                        " .note-editable",
                    run: "text Draft other matter narrative for this engagement.",
                },

                // Flow 5 - Click Save
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // Post-Condition - the record is saved
                {
                    content: "Worksheet is saved",
                    trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );

        // IK (ssi_general_audit_worksheet_final_report module):
        // docs/general_audit_ws_b66777d/01-fill-final-opinion.md
        //
        // Lives in THIS module's tour file, not
        // ssi_general_audit_worksheet_final_report's, because
        // ssi_general_audit_worksheet_review depends on
        // ssi_general_audit_worksheet_final_report -- never the other
        // way around -- so this is the only place a fc75636 sibling
        // worksheet (the Populate button's copy source) can exist
        // for the tour's setUpClass fixture. See
        // GeneralAuditWSb66777d._populate_final_opinion()'s docstring.
        tour.register(
            "ssi_general_audit_worksheet_review_b66777d_fill_final_opinion",
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

                // Flow 2 - Open the worksheet to fill the final audit
                // opinion for
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

                // Flow 3 - Open the Final Audit Opinion tab
                {
                    content: "Open the Final Audit Opinion tab",
                    trigger: ".o_notebook .nav-link:contains(Final Audit Opinion)",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 - Click Populate. This is an object-type button
                // that writes the nine fields asynchronously, so the
                // next step's trigger must name something that only
                // exists AFTER the write lands -- here, the Opinion
                // field's note-editable actually carrying the exact
                // text copied from this engagement's fc75636 sibling
                // (setUpClass fixture), not just the empty widget the
                // form already renders before Populate is clicked. See
                // odoo-development-ui-test skill
                // patterns-advanced-gotchas.md §P.
                {
                    content: "Click the Populate button",
                    trigger:
                        ".o_form_view button[name='action_populate_final_opinion']",
                    extra_trigger: ".o_form_view",
                },
                {
                    content: "Opinion field is filled by Populate",
                    trigger:
                        ".tab-pane.active " +
                        ".o_field_widget[name='opinion'] " +
                        ".note-editable:contains(Populate tour source text - Opinion)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 5 - Edit one of the nine fields manually after
                // Populate
                {
                    content: "Edit the Opinion field manually after Populate",
                    trigger:
                        ".tab-pane.active " +
                        ".o_field_widget[name='opinion'] .note-editable",
                    run: "text Opinion narrative, edited manually after Populate.",
                },

                // Flow 6 - Click Save
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // Post-Condition - the record is saved
                {
                    content: "Worksheet is saved",
                    trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );
    }
);
