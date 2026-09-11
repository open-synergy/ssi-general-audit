/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html). */

odoo.define(
    "ssi_general_audit_worksheet_review.general_audit_ws_a025441_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/general_audit_ws_a025441/02-edit.md
        tour.register(
            "ssi_general_audit_worksheet_review_a025441_fill_disclosure_checklist",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 - Open the Windup & Reporting > Review >
                // Financial Statement Disclosure menu.
                //
                // "Review" (level 2) has children (Financial Statement
                // Disclosure, Audit Evidence), so it renders as a
                // clickable dropdown-toggle section. "Financial
                // Statement Disclosure" (level 3, menu_general_audit_
                // final_disclosure) also has a child
                // (general_audit_ws_a025441_menu), so it renders as an
                // unclickable grouping header WITHOUT data-menu-xmlid --
                // it gets no step of its own. The leaf
                // (general_audit_ws_a025441_menu, level 4) is a clickable
                // item inside the "Review" dropdown. See
                // odoo-development-ui-test skill
                // references/patterns-navigation-and-form.md §A.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Windup & Reporting app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_general_audit.menu_wind_up_reporting_root"]',
                },
                {
                    content: "Open the Review menu",
                    trigger:
                        ".o_menu_sections " +
                        "[data-menu-xmlid='ssi_general_audit.menu_general_audit_review']",
                },
                {
                    content: "Open the Financial Statement Disclosure menu",
                    trigger:
                        ".o_menu_sections " +
                        "[data-menu-xmlid='ssi_general_audit_worksheet_review" +
                        ".general_audit_ws_a025441_menu']",
                },
                {
                    // Gate: wait for the TARGET action, not just any list
                    // view -- clicking Review lands on its first
                    // sub-menu first.
                    content: "Financial Statement Disclosure list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active" +
                        ":contains(Financial Statement Disclosure)",
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
                {
                    // Financial_accounting_standard_id -- related, read-only
                    // display of the engagement's standard, shown below
                    // Reviewer so the auditor knows which checklist variant
                    // to paste. Value comes from setUpClass's
                    // "Test Standard - A025441 Tour" fixture.
                    content: "Financial Accounting Standard is shown",
                    trigger:
                        ".o_field_widget[name='financial_accounting_standard_id']" +
                        ":contains(Test Standard - A025441 Tour)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 3 - Click the Edit button
                //
                // 14.0: an opened existing record is READONLY until Edit
                // is clicked -- unlike Create, which opens editable
                // directly. See odoo-development-ui-test skill
                // references/patterns-navigation-and-form.md §E.
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

                // Flow 4 - Open the Checklist tab, then paste the
                // completed disclosure checklist CSV into Raw Data.
                //
                // "Checklist" is the first notebook page, so it is
                // already active on load -- the click is still issued
                // per odoo-development-ui-test skill
                // references/patterns-fields.md §Jebakan 1c (safe even
                // when the page happens to already be active).
                {
                    content: "Open the Checklist tab",
                    trigger: ".o_notebook .nav-link:contains(Checklist)",
                },
                //
                // widget="csv_table" (FieldCsvTable) switches its own
                // tagName to "div" in edit mode so it can nest a toggle
                // bar next to the real <textarea class=
                // "csv_table_textarea"> -- unlike a plain Text field,
                // the root .o_field_widget here is NOT itself the input,
                // so the " textarea" suffix is required (not the usual
                // exception -- see odoo-development-ui-test skill
                // references/patterns-fields.md §C, Text row).
                //
                // `run` is a FUNCTION here, not a "text ..." string --
                // deliberately, not stylistically. Odoo 14's tour engine
                // parses a string `run` with a regex that has no /s or
                // /m flag (tour_manager.js ~line 499:
                // /^([a-zA-Z0-9_]+) *(?:\(? *(.+?) *\)?)?$/), so "." never
                // matches "\n": a multi-line CSV payload makes the regex
                // return null and the very next line's `m[1]` throws
                // "Cannot read properties of null (reading '1')" --
                // deterministically, proven from two full CI runs
                // (PR #327, run 34603243888) where this was the ONLY
                // failure and it recurred at the identical point on an
                // unchanged-code rerun (ruling out the registered S-01
                // core race, which has a different message entirely:
                // "Cannot SET properties of null (setting 'props')").
                // The function form bypasses that regex parser
                // completely (tour_manager.js branches on
                // `typeof tip.run === "function"` before ever reaching
                // it) and calls the same underlying helper
                // (`RunningTourActionHelper.text`,
                // running_tour_action_helper.js) directly.
                {
                    content: "Paste the disclosure checklist CSV into Raw Data",
                    trigger: ".o_field_widget[name='raw_data'] textarea",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: function (actions) {
                        actions.text(
                            "Item,Standard,Note,Status\n" +
                                "PSAK 1 - Basis of preparation,PSAK 1,Note 2,Yes"
                        );
                    },
                },

                // Flow 5 - Select the Conclusion (conclusion_id, inherited
                // generically from general_audit_worksheet -- master data
                // for worksheet_type_a025441 already ships with the module,
                // see data/master/general_audit_worksheet_conclusion.xml).
                {
                    content: "Open the Conclusion dropdown",
                    trigger: ".o_field_many2one[name='conclusion_id'] input",
                    run: "text Financial Statement Disclosure has been completed",
                },
                {
                    content: "Pick the Conclusion from the dropdown",
                    trigger:
                        ".ui-autocomplete:visible " +
                        "li a:contains(Financial Statement Disclosure has been completed)",
                    in_modal: false,
                },

                // Flow 6 - Fill in the Conclusion narrative text
                {
                    content: "Fill in the Conclusion narrative",
                    trigger: ".o_field_widget[name='conclusion']",
                    run: "text All disclosure items reviewed and documented.",
                },

                // Flow 7 - Save
                {
                    content: "Save the worksheet",
                    trigger: ".o_form_button_save",
                },
                {
                    content: "Worksheet is saved",
                    trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Post-Condition - Raw Data, Conclusion (m2o) and the
                // Conclusion narrative show the saved values. csv_table
                // renders plain <td> text cells in readonly mode (not
                // <input class="csv_table_cell_input">, which only
                // exists in edit mode) -- assert on the <td> text, on
                // the data row (row 0 is the header).
                {
                    content: "Raw Data shows the saved disclosure checklist row",
                    trigger:
                        ".o_field_widget[name='raw_data'] " +
                        "td:contains(PSAK 1 - Basis of preparation)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Conclusion shows the saved selection",
                    trigger:
                        ".o_field_widget[name='conclusion_id']" +
                        ":contains(Financial Statement Disclosure has been completed)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Conclusion narrative shows the saved text",
                    trigger:
                        ".o_field_widget[name='conclusion']" +
                        ":contains(All disclosure items reviewed and documented.)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );
    }
);
