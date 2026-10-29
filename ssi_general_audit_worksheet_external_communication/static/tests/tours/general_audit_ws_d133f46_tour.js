/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html). */

odoo.define(
    "ssi_general_audit_worksheet_external_communication.general_audit_ws_d133f46_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/general_audit_ws_d133f46/01-create.md
        tour.register(
            "ssi_general_audit_worksheet_external_communication_d133f46_create",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 - Open the Risk Assessment > External Communication > Use of Internal Auditor's Work Results menu.
                // "External Communication" (has children) renders as a
                // dropdown section; the leaf below it has
                // data-menu-xmlid and is directly clickable.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Risk Assessment app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_general_audit.menu_risk_assesment_root"]',
                },
                {
                    // The Risk Assessment app has more level-1 sections than
                    // fit the navbar, so External Communication is folded into
                    // the "+" overflow dropdown. Open it only when the section
                    // is not directly visible; otherwise the section itself
                    // matches first and nothing is clicked here.
                    content:
                        "Open the overflow menu if External Communication is folded",
                    trigger:
                        ".o_menu_sections > li > " +
                        '[data-menu-xmlid="ssi_general_audit.menu_general_audit_ra_external_communication"], ' +
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
                    // clicks (navbar.scss), so only wait for it.
                    content:
                        "Open the External Communication section if it is not folded",
                    trigger:
                        ".o_menu_sections > li > " +
                        '[data-menu-xmlid="ssi_general_audit.menu_general_audit_ra_external_communication"]' +
                        ":not(.dropdown-item), " +
                        ".o_menu_sections li.o_extra_menu_items.show > ul",
                    run: function () {
                        if (this.$anchor.is("[data-menu-xmlid]")) {
                            this.$anchor[0].click();
                        }
                    },
                },
                {
                    content: "Open the Use of Internal Auditor's Work Results menu",
                    trigger:
                        ".o_menu_sections " +
                        "[data-menu-xmlid='ssi_general_audit_worksheet_external_communication" +
                        ".general_audit_ws_d133f46_menu']",
                },
                {
                    content: "The worksheet list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Work Results)",
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
                    run: "text TOUR-D133F46-GA",
                },
                {
                    content: "Pick the General Audit from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR-D133F46-GA)",
                    in_modal: false,
                },

                // Flow 4/5 - Save. The auto-filled Accountant, Partner and
                // Title values are not asserted: tours do not test values.
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
            ]
        );
    }
);
