/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html). */

odoo.define(
    "ssi_general_audit_worksheet_audit_procedure_inquiry.general_audit_ws_a145276_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/general_audit_ws_a145276/01-create.md
        tour.register(
            "ssi_general_audit_worksheet_audit_procedure_inquiry_a145276_create",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 - Open the Risk Responses > General Procedures > Inquiry menu.
                // "General Procedures" (has children) renders as a dropdown
                // section; the leaf below it has data-menu-xmlid and is
                // directly clickable.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Risk Responses app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_general_audit.menu_risk_responses_root"]',
                },
                {
                    // The Risk Responses app has more level-1 sections than
                    // fit the navbar, so General Procedures may be folded into the
                    // "+" overflow dropdown. Open it only when the section is
                    // not directly visible.
                    content: "Open the overflow menu if General Procedures is folded",
                    trigger:
                        ".o_menu_sections > li > " +
                        '[data-menu-xmlid="ssi_general_audit_worksheet_lead_schedule.general_audit_audit_procedure_root_menu"], ' +
                        ".o_menu_sections li.o_extra_menu_items > a",
                    run: function () {
                        if (this.$anchor.closest("li").hasClass("o_extra_menu_items")) {
                            this.$anchor[0].click();
                        }
                    },
                },
                {
                    // Directly visible: click the section to open its
                    // dropdown. Folded: the opened "+" dropdown already lists
                    // every section expanded and its section headers ignore
                    // clicks, so only wait for it.
                    content: "Open the General Procedures section if it is not folded",
                    trigger:
                        ".o_menu_sections > li > " +
                        '[data-menu-xmlid="ssi_general_audit_worksheet_lead_schedule.general_audit_audit_procedure_root_menu"]' +
                        ":not(.dropdown-item), " +
                        ".o_menu_sections li.o_extra_menu_items.show > ul",
                    run: function () {
                        if (this.$anchor.is("[data-menu-xmlid]")) {
                            this.$anchor[0].click();
                        }
                    },
                },
                {
                    content: "Open the Inquiry menu",
                    trigger:
                        ".o_menu_sections " +
                        "[data-menu-xmlid='ssi_general_audit_worksheet_audit_procedure_inquiry" +
                        ".general_audit_ws_a145276_menu']",
                },
                {
                    content: "The worksheet list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Inquiry Audit Procedures)",
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
                    run: "text TOUR-A145276-GA",
                },
                {
                    content: "Pick the General Audit from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR-A145276-GA)",
                    in_modal: false,
                },

                // Flow 4/5 - Save. The auto-filled Accountant, Partner and
                // Title values are not asserted: tours do not test values.
                {
                    content: "General Audit is filled before saving",
                    trigger: ".o_field_many2one[name='general_audit_id'] input",
                    extra_trigger:
                        ".o_field_many2one[name='general_audit_id'] .o_external_button",
                    run: function () {
                        if (this.$anchor.val().indexOf("TOUR-A145276-GA") < 0) {
                            throw new Error("General Audit is not filled");
                        }
                    },
                },
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // Proof that the record was really saved: the pager appears
                // and the breadcrumb is no longer "New".
                {
                    content: "The record is saved (pager shown)",
                    trigger: ".o_control_panel .o_pager_counter",
                    extra_trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "The breadcrumb is not New",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:not(:contains(New))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
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
            ]
        );
    }
);
