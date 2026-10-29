/* Copyright 2026 OpenSynergy Indonesia
 Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html). */

odoo.define(
    "ssi_general_audit_worksheet_client_package.general_audit_ws_b5e3d9f_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/general_audit_ws_b5e3d9f/01-create.md
        tour.register(
            "ssi_general_audit_worksheet_client_package_b5e3d9f_create",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 - Open the Risk Assessment > Client Assistance Package > Subledgers menu.
                // "Client Assistance Package" (has children) renders as a dropdown
                // section; the leaf inside it has data-menu-xmlid and is
                // directly clickable.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Risk Assessment app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_general_audit.menu_risk_assesment_root"]',
                },
                {
                    // The Risk Assessment app may have more level-1 sections than
                    // fit the navbar, so Client Assistance Package may be folded
                    // into the "+" overflow dropdown. Open it only when the
                    // section is not directly visible; otherwise the section
                    // itself matches first and nothing is clicked here.
                    content:
                        "Open the overflow menu if Client Assistance Package is folded",
                    trigger:
                        ".o_menu_sections > li > " +
                        '[data-menu-xmlid="ssi_general_audit.menu_general_audit_client_package"], ' +
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
                        "Open the Client Assistance Package section if it is not folded",
                    trigger:
                        ".o_menu_sections > li > " +
                        '[data-menu-xmlid="ssi_general_audit.menu_general_audit_client_package"]' +
                        ":not(.dropdown-item), " +
                        ".o_menu_sections li.o_extra_menu_items.show > ul",
                    run: function () {
                        if (this.$anchor.is("[data-menu-xmlid]")) {
                            this.$anchor[0].click();
                        }
                    },
                },
                {
                    content: "Open the Subledgers menu",
                    trigger:
                        ".o_menu_sections " +
                        "[data-menu-xmlid='ssi_general_audit_worksheet_client_package" +
                        ".general_audit_ws_b5e3d9f_menu']",
                },
                {
                    content: "The worksheet list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Subledgers)",
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
                    run: "text TOUR-B5E3D9F-GA",
                },
                {
                    content: "Pick the General Audit from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR-B5E3D9F-GA)",
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
