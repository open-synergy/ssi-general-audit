/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html). */

odoo.define(
    "ssi_general_audit_worksheet_physical_check.general_audit_ws_c7d5f2b_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/general_audit_ws_c7d5f2b/01-isi-data-perbandingan.md
        tour.register(
            "ssi_general_audit_worksheet_physical_check_c7d5f2b_fill_data_comparison",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 - Open the Risk Responses > General Procedures >
                // Inspection > Physical Check menu.
                //
                // "General Procedures" (level 2) has children (Inspection),
                // so it renders as a clickable dropdown-toggle section.
                // "Inspection" (level 3) also has children (Vouching,
                // Physical Check), so it renders as an unclickable grouping
                // header WITHOUT data-menu-xmlid -- it gets no step of its
                // own. "Physical Check" (level 4) is a leaf, rendered as a
                // clickable item inside the "General Procedures" dropdown.
                // See odoo-development-ui-test-skill
                // references/patterns-navigation-and-form.md §A.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Risk Responses app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_general_audit.menu_risk_responses_root"]',
                },
                {
                    content: "Open the General Procedures menu",
                    trigger:
                        ".o_menu_sections " +
                        "[data-menu-xmlid='ssi_general_audit_worksheet_lead_schedule" +
                        ".general_audit_audit_procedure_root_menu']",
                },
                {
                    content: "Open the Physical Check menu",
                    trigger:
                        ".o_menu_sections " +
                        "[data-menu-xmlid='ssi_general_audit_worksheet_physical_check" +
                        ".general_audit_ws_c7d5f2b_menu']",
                },
                {
                    // Gate: wait for the TARGET action, not just any list
                    // view -- clicking General Procedures lands on its
                    // first sub-menu first.
                    content: "Physical Check list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Physical Check)",
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
                    // 14.0: an opened existing record is READONLY until Edit
                    // is clicked -- unlike Create, which opens editable
                    // directly. See odoo-development-ui-test-skill
                    // references/patterns-navigation-and-form.md §E.
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

                // Flow 3 - Select Data Mode = General Ledger
                {
                    content: "Select Data Mode = General Ledger",
                    trigger: "select.o_field_widget[name='data_mode']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text General Ledger",
                },

                // Flow 4 - Select the matching General Ledger record (the
                // population/reference source). display_name here is the
                // worksheet's document number ("/" until action_open/
                // action_confirm assign one -- see mixin_transaction
                // name_get), NOT a fixture field, so it cannot be typed or
                // matched by :contains. Two General Ledger worksheets exist
                // on this engagement (this one, and the comparison one used
                // later in the Data Comparison line); _order on the model
                // is "general_audit_id, parent_type_id, id", both share
                // general_audit_id/parent_type_id, so the one created FIRST
                // in Python (ref_gl) sorts first -- pick it positionally.
                {
                    content: "Open the General Ledger dropdown",
                    trigger: ".o_field_many2one[name='general_ledger_id'] input",
                    run: "click",
                },
                {
                    content: "Pick the Reference General Ledger (created first)",
                    trigger:
                        ".ui-autocomplete:visible " +
                        ".ui-menu-item:not(.o_m2o_start_typing) a:eq(0)",
                    in_modal: false,
                },

                // Flow 5 - Select Data Source = Sample
                {
                    content: "Select Data Source = Sample",
                    trigger: "select.o_field_widget[name='data_source']",
                    run: "text Sample",
                },

                // Flow 6 - Select the Sample Determination and fill the
                // Reference Column Number
                {
                    content: "Open the Sample Determination dropdown",
                    trigger: ".o_field_many2one[name='sample_determination_id'] input",
                    run: "click",
                },
                {
                    content: "Pick the only allowed Sample Determination",
                    trigger:
                        ".ui-autocomplete:visible " +
                        ".ui-menu-item:not(.o_m2o_start_typing) a:eq(0)",
                    in_modal: false,
                },
                {
                    content: "Fill in the Reference Column Number",
                    trigger: ".o_field_widget[name='reference_col_number']",
                    run: "text 1",
                },

                // Flow (Save before leaving the worksheet form)
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

                // Flow 7 - Open Data Comparisons
                //
                // action_open_data_comparisons lives inside the "Data
                // Comparisons" notebook page (3rd tab) -- after Save the
                // active tab is still "Raw Data" (1st tab), so the button
                // exists in the DOM but is hidden inside a non-active
                // .tab-pane. Activate its tab first (safe even when the
                // tab already happens to be active). See
                // odoo-development-ui-test-skill
                // references/patterns-fields.md "Jebakan 1c".
                {
                    content: "Open the Data Comparisons tab",
                    trigger: ".o_notebook .nav-link:contains(Data Comparisons)",
                    extra_trigger: ".o_form_view.o_form_readonly",
                },
                {
                    content: "Click the Open Data Comparisons button",
                    trigger:
                        ".tab-pane.active button[name='action_open_data_comparisons']",
                    extra_trigger: ".o_form_view",
                },
                {
                    content: "Data Comparisons list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Data Comparisons)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 8 - Create a Data Comparison line
                {
                    content: "Click Create on Data Comparisons",
                    trigger: ".o_list_button_add",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Data Comparison form is open in edit mode",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 9 - Fill the Data Comparison's own Data Mode /
                // General Ledger / Reference Column Number
                {
                    content: "Select Data Comparison Data Mode = General Ledger",
                    trigger: "select.o_field_widget[name='data_mode']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text General Ledger",
                },
                // Same display_name caveat as Flow 4: pick the comparison
                // GL (ref_gl created first, cmp_gl created second, same
                // _order tiebreak) positionally, not by typed text.
                {
                    content: "Open the comparison General Ledger dropdown",
                    trigger: ".o_field_many2one[name='general_ledger_id'] input",
                    run: "click",
                },
                {
                    content: "Pick the Comparison General Ledger (created second)",
                    trigger:
                        ".ui-autocomplete:visible " +
                        ".ui-menu-item:not(.o_m2o_start_typing) a:eq(1)",
                    in_modal: false,
                },
                {
                    content: "Fill in the Data Comparison's Reference Column Number",
                    trigger: ".o_field_widget[name='reference_col_number']",
                    run: "text 1",
                },
                {
                    content: "Save the Data Comparison",
                    trigger: ".o_form_button_save",
                },
                {
                    content: "Data Comparison is saved",
                    trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 10 - Go back to the worksheet (breadcrumb item #2:
                // Physical Check > worksheet > Data Comparisons > [record]).
                {
                    content: "Go back to the worksheet",
                    trigger:
                        ".o_control_panel ol.breadcrumb li.breadcrumb-item:nth-child(2)",
                },
                {
                    content: "Worksheet form is displayed again",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 10 (cont.) - Open Check Lines
                //
                // Same cause as the Data Comparisons button above:
                // action_open_check_lines lives inside the "Check" notebook
                // page, and the breadcrumb click just above reloads the
                // worksheet form back to its first tab ("Raw Data").
                // Activate the "Check" tab before clicking its button.
                //
                // :contains(Check) ALONE also matches the "Check Items"
                // tab (substring match, and it sorts earlier: Raw Data,
                // Check Items, Data Comparisons, Check, Findings, ...) --
                // jQuery :contains returns the FIRST DOM match, so a bare
                // :contains(Check) silently opens "Check Items" instead,
                // leaving the real "Check" tab-pane inactive. Exclude it.
                {
                    content: "Open the Check tab",
                    trigger:
                        ".o_notebook .nav-link:contains(Check):not(:contains(Items))",
                    extra_trigger: ".o_form_view.o_form_readonly",
                },
                {
                    content: "Click the Open Check Lines button",
                    trigger: ".tab-pane.active button[name='action_open_check_lines']",
                    extra_trigger: ".o_form_view",
                },
                {
                    content: "Check Lines list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Check Lines)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 11 - Create a Check line
                {
                    content: "Click Create on Check Lines",
                    trigger: ".o_list_button_add",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Check Line form is open in edit mode",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 12 - Select the Comparison Mode and amount columns
                // FIRST, then the Data Comparison last.
                //
                // Order matters here, and it is not cosmetic: every other
                // many2one on this tour whose domain depends on a computed
                // "allowed_*_ids" field (general_ledger_id/
                // sample_determination_id on the worksheet, general_ledger_id
                // on the Data Comparison line) is opened only AFTER the user
                // has already triggered a SECOND onchange round-trip on that
                // record (by picking Data Mode/Data Source beforehand) -- and
                // all three succeed. data_comparison_id here is the only
                // many2one of this kind opened right after the record's
                // FIRST (creation) onchange, with no intervening field
                // change, and that is exactly the one that failed in CI
                // (name_search on general_audit_ws_c7d5f2b.data_comparison
                // returned no matches even though allowed_data_comparison_ids
                // resolves correctly server-side -- verified via `odoo shell`
                // onchange() simulation). Selecting Comparison Mode first
                // reproduces the same successful pattern: it is a plain
                // <select> field change, which triggers its own onchange
                // round-trip before the Data Comparison dropdown is ever
                // opened.
                {
                    content: "Select Comparison Mode = Sum",
                    trigger: "select.o_field_widget[name='comparison_mode']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text Sum",
                },
                {
                    content: "Fill in the Reference Amount Column",
                    trigger: ".o_field_widget[name='reference_amount_col']",
                    run: "text 2",
                },
                {
                    content: "Fill in the Comparison Amount Column",
                    trigger: ".o_field_widget[name='comparison_amount_col']",
                    run: "text 2",
                },

                // Flow 12 (cont.) - Select the Data Comparison last, after
                // the Comparison Mode onchange above has already run. Only
                // ONE Data Comparison line exists at this point (the single
                // one created in Flow 8-9), and its own display_name is a
                // non-typeable document number/"-" -- pick it positionally,
                // same as Sample Determination in Flow 6.
                {
                    content: "Open the Data Comparison dropdown",
                    trigger: ".o_field_many2one[name='data_comparison_id'] input",
                    run: "click",
                },
                {
                    content: "Pick the only Data Comparison from the dropdown",
                    trigger:
                        ".ui-autocomplete:visible " +
                        ".ui-menu-item:not(.o_m2o_start_typing) a:eq(0)",
                    in_modal: false,
                },
                {
                    content: "Save the Check Line",
                    trigger: ".o_form_button_save",
                },
                {
                    content: "Check Line is saved",
                    trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 13 - Click the Compute Check Data button
                {
                    content: "Click the Compute Check Data button",
                    trigger: "button[name='action_compute_check_data']",
                    extra_trigger: ".o_form_view",
                },

                // Post-Condition - the Check Data field is filled with the
                // CSV comparison result. The gate below can only ever match
                // AFTER Compute is clicked: the check line is freshly
                // created with no Check Data yet, and the reference value
                // asserted here only exists after the comparison runs.
                {
                    content: "Check Data shows the computed comparison row",
                    trigger:
                        ".o_field_widget[name='check_data'] " +
                        "input.csv_table_cell_input[value='TOUR-C7D5F2B-R1']",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );
    }
);
