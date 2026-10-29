/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html). */

odoo.define(
    "ssi_general_audit_worksheet_understanding_entity.general_audit_ws_e78a3c6_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/general_audit_ws_e78a3c6/01-create.md
        tour.register(
            "ssi_general_audit_worksheet_understanding_entity_e78a3c6_create",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 - Open the Risk Assessment > Understanding The Entity > Structure Organization and Responsibilities menu.
                // "Understanding The Entity" (has children) renders as a
                // dropdown section; the leaf below it has
                // data-menu-xmlid and is directly clickable.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Risk Assessment app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_general_audit.menu_risk_assesment_root"]',
                },
                {
                    content: "Open the Understanding The Entity menu",
                    trigger:
                        ".o_menu_sections " +
                        '[data-menu-xmlid="ssi_general_audit.menu_general_audit_understanding_entity"]',
                },
                {
                    content:
                        "Open the Structure Organization and Responsibilities menu",
                    trigger:
                        ".o_menu_sections " +
                        "[data-menu-xmlid='ssi_general_audit_worksheet_understanding_entity" +
                        ".general_audit_ws_e78a3c6_menu']",
                },
                {
                    content: "The worksheet list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Structure Organization)",
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
                    run: "text TOUR-E78A3C6-GA",
                },
                {
                    content: "Pick the General Audit from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR-E78A3C6-GA)",
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
