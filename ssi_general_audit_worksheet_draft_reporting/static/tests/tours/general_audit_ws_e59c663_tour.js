/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html). */

odoo.define(
    "ssi_general_audit_worksheet_draft_reporting.general_audit_ws_e59c663_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // Shared helper: the x2many row-edit dialog's primary button is
        // labelled "Save & Close" for a NEW row and "Save" for an EXISTING
        // one (view_dialogs.js:131) -- our checklist rows always have a
        // res_id (populated by action_populate_checklist), so "Save" is
        // used here, but the helper accepts both so it stays correct if
        // that ever changes. No ".modal" prefix on the trigger -- see
        // odoo-development-ui-test-skill patterns-dialogs-and-wizards.md §H.
        function clickDialogSaveStep(content) {
            return {
                content: content,
                trigger: ".modal-footer button.btn-primary",
                run: function () {
                    var $btn = $(".modal:visible")
                        .last()
                        .find(".modal-footer button.btn-primary")
                        .filter(function () {
                            var t = $(this).text().trim();
                            return t === "Save & Close" || t === "Save";
                        });
                    $btn[0].click();
                },
            };
        }

        // IK: docs/general_audit_ws_e59c663/01-create.md
        tour.register(
            "ssi_general_audit_worksheet_draft_reporting_e59c663_create",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 - Open the Windup & Reporting > Draft Reporting >
                // Draft Financial Statements menu. "Draft Reporting" (has
                // children) renders as a dropdown section; the leaf below
                // it has data-menu-xmlid and is directly clickable -- see
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
                    content: "Open the Draft Financial Statements menu",
                    trigger:
                        ".o_menu_sections " +
                        "[data-menu-xmlid='ssi_general_audit_worksheet_draft_reporting" +
                        ".general_audit_ws_e59c663_menu']",
                },
                {
                    content: "Draft Financial Statements list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Draft Financial Statements)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 2 - Click the Create button. (14.0 label: "Create")
                {
                    content: "Click the Create button",
                    trigger: ".o_list_button_add",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "A new record form is open",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 3 - Fill in the required General Audit field.
                {
                    content: "Select the General Audit",
                    trigger: ".o_field_many2one[name='general_audit_id'] input",
                    run: "text Test General Audit - E59C663 Tour",
                },
                {
                    content: "Pick the General Audit from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(Test General Audit - E59C663 Tour)",
                    in_modal: false,
                },

                // Flow 4 - Accountant/Partner/Title are auto-filled from
                // the selected General Audit -- assertion only, no input.
                {
                    content: "Accountant is auto-filled",
                    trigger:
                        ".o_field_widget[name='accountant_id']:contains(Test Audit Accountant - E59C663 Tour)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 5 - Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // Post-Condition - a new record is created in Draft status.
                {
                    content: "Status is Draft",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Post-Condition - both the Completeness checklist
                // (WR.160.1) and Review Procedure Checklist (WR.160) tabs
                // are visible on the form, even though both are still
                // empty at this point.
                {
                    content: "The Completeness checklist tab is visible",
                    trigger: ".o_notebook .nav-link:contains(Completeness)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "The Review Procedure Checklist tab is visible",
                    trigger:
                        ".o_notebook .nav-link:contains(Review Procedure Checklist)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );

        // IK: docs/general_audit_ws_e59c663/08-open.md
        tour.register(
            "ssi_general_audit_worksheet_draft_reporting_e59c663_open",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 - Open the Windup & Reporting > Draft Reporting >
                // Draft Financial Statements menu.
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
                    content: "Open the Draft Financial Statements menu",
                    trigger:
                        ".o_menu_sections " +
                        "[data-menu-xmlid='ssi_general_audit_worksheet_draft_reporting" +
                        ".general_audit_ws_e59c663_menu']",
                },

                // Flow 2 - Open the record to start. setUpClass leaves
                // exactly one Draft-state e59c663 worksheet (worksheet_draft);
                // its state badge text is the only stable anchor since the
                // document number is still "/" before Start assigns one.
                {
                    content: "Open the draft worksheet",
                    trigger: ".o_data_row:contains(Draft) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Worksheet form is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 3 - Click the Start button.
                {
                    content: "Click the Start button",
                    trigger: ".o_statusbar_buttons button[name='action_open']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 - Click OK on the confirmation dialog
                // (action_open carries confirm="Start data. Are you sure?").
                // No ".modal" prefix -- 14.0, see patterns-dialogs-and-wizards.md §H.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Assertion - status is now On Progress (open). Gated on the
                // modal being closed -- §K.
                {
                    content: "Status is On Progress",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='open'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 5 - Open the Review Procedure Checklist tab (WR.160,
                // now the first checklist tab on the form). Both tab
                // labels are unique substrings of each other
                // ("Review Procedure Checklist" vs. "Completeness of
                // financial statements cheklist"), so no disambiguation
                // (":not(...)") is needed for either trigger.
                {
                    content: "Open the Review Procedure Checklist tab",
                    trigger:
                        ".o_notebook .nav-link:contains(Review Procedure Checklist)",
                    extra_trigger: ".o_form_view",
                },

                // Flow 6 - Click the Populate button. review_checklist_ids
                // is EMPTY before this worksheet is started (populate has
                // never run on it), so a row appearing is a gate that is
                // impossible to satisfy before the click -- see
                // patterns-advanced-gotchas.md §P "uji lakmus gerbang".
                {
                    content: "Click the Populate button (review checklist)",
                    trigger:
                        ".tab-pane.active " +
                        "button[name='action_populate_review_checklist']",
                    extra_trigger: ".tab-pane.active",
                },
                {
                    content: "Review checklist rows are populated from the master",
                    trigger:
                        ".tab-pane.active .o_field_widget[name='review_checklist_ids'] " +
                        ".o_data_row:contains(Perform footing)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 7 - On the first review checklist row, set the
                // Option field. The tree has no `editable` attribute, so
                // clicking a row opens its paired <form> in a dialog -- see
                // patterns-navigation-and-form.md "Save di dalam DIALOG".
                {
                    content: "Open the first review checklist row",
                    trigger:
                        ".tab-pane.active .o_field_widget[name='review_checklist_ids'] " +
                        ".o_data_row:contains(Perform footing) .o_data_cell:first",
                },
                {
                    content: "Review checklist row dialog is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Select the Yes option",
                    trigger: ".o_field_widget[name='option_id'] input",
                    run: "text Yes",
                },
                {
                    content: "Pick Yes from the dropdown",
                    trigger: ".ui-autocomplete .ui-menu-item a:contains(Yes)",
                    in_modal: false,
                },
                clickDialogSaveStep("Save the review checklist row"),

                // Post-Condition - the row shows the saved answer, and the
                // dialog is closed.
                {
                    content: "The review checklist row shows the saved answer",
                    trigger:
                        ".tab-pane.active .o_field_widget[name='review_checklist_ids'] " +
                        ".o_data_row:contains(Perform footing):contains(Yes)",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 8 - Open the Completeness checklist tab (WR.160.1,
                // second checklist tab on the form).
                {
                    content: "Open the Completeness checklist tab",
                    trigger: ".o_notebook .nav-link:contains(Completeness)",
                    extra_trigger: ".o_form_view",
                },

                // Flow 9 - Click the Populate button. checklist_ids is
                // EMPTY before this click, so a row appearing is a gate
                // impossible to satisfy beforehand -- same lakmus test as
                // Flow 6 above (patterns-advanced-gotchas.md §P).
                {
                    content: "Click the Populate button",
                    trigger:
                        ".tab-pane.active button[name='action_populate_checklist']",
                    extra_trigger: ".tab-pane.active",
                },
                {
                    content: "Checklist rows are populated from the master",
                    trigger:
                        ".tab-pane.active .o_field_widget[name='checklist_ids'] " +
                        ".o_data_row:contains(Report Cover)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 10 - On the first checklist row, set the Option
                // field.
                {
                    content: "Open the first checklist row",
                    trigger:
                        ".tab-pane.active .o_field_widget[name='checklist_ids'] " +
                        ".o_data_row:contains(Report Cover) .o_data_cell:first",
                },
                {
                    content: "Checklist row dialog is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Select the Present option",
                    trigger: ".o_field_widget[name='option_id'] input",
                    run: "text Present",
                },
                {
                    content: "Pick Present from the dropdown",
                    trigger: ".ui-autocomplete .ui-menu-item a:contains(Present)",
                    in_modal: false,
                },
                clickDialogSaveStep("Save the checklist row"),

                // Post-Condition - the row shows the saved answer, and the
                // dialog is closed.
                {
                    content: "The checklist row shows the saved answer",
                    trigger:
                        ".tab-pane.active .o_field_widget[name='checklist_ids'] " +
                        ".o_data_row:contains(Report Cover):contains(Present)",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );

        // IK: docs/general_audit_ws_e59c663/04-confirm.md
        tour.register(
            "ssi_general_audit_worksheet_draft_reporting_e59c663_confirm",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 - Open the Windup & Reporting > Draft Reporting >
                // Draft Financial Statements menu.
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
                    content: "Open the Draft Financial Statements menu",
                    trigger:
                        ".o_menu_sections " +
                        "[data-menu-xmlid='ssi_general_audit_worksheet_draft_reporting" +
                        ".general_audit_ws_e59c663_menu']",
                },

                // Flow 2 - Open the record to confirm. setUpClass leaves
                // exactly one On Progress e59c663 worksheet (worksheet_open).
                {
                    content: "Open the on-progress worksheet",
                    trigger: ".o_data_row:contains(On Progress) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Worksheet form is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 3 - Fill in Conclusion and the notes field.
                {
                    content: "Select the Conclusion",
                    trigger: ".o_field_many2one[name='conclusion_id'] input",
                    run: "text Complete - E59C663 Tour",
                },
                {
                    content: "Pick the Conclusion from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(Complete - E59C663 Tour)",
                    in_modal: false,
                },
                {
                    content: "Fill in the Conclusion notes",
                    trigger: ".o_field_widget[name='conclusion'] textarea",
                    run: "text Draft financial statements reviewed against WR.160.1.",
                },

                // Flow 4 - Click the Confirm button.
                {
                    content: "Click the Confirm button",
                    trigger: ".o_statusbar_buttons button[name='action_confirm']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 5 - Click OK on the confirmation dialog
                // (action_confirm carries confirm="Confirm data. Are you sure?").
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition - status is Waiting for Approval (confirm).
                {
                    content: "Status is Waiting for Approval",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Post-Condition - both the Completeness checklist
                // (WR.160.1) and Review Procedure Checklist (WR.160) tabs,
                // and their answers, remain visible after confirming.
                {
                    content: "The Completeness checklist tab is still visible",
                    trigger: ".o_notebook .nav-link:contains(Completeness)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "The Review Procedure Checklist tab is still visible",
                    trigger:
                        ".o_notebook .nav-link:contains(Review Procedure Checklist)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );
    }
);
