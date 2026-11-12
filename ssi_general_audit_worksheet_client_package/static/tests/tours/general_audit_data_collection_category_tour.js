/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html). */

odoo.define(
    "ssi_general_audit_worksheet_client_package.general_audit_data_collection_category_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/general_audit_data_collection_category/01-create.md
        tour.register(
            "ssi_general_audit_worksheet_client_package_data_collection_category_create",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 - Open the Configuration > Standard & Regulation > Data Collections > Data Collection Categories menu.
                // "Standard & Regulation" (has children) renders as a dropdown
                // section; the leaf below it has data-menu-xmlid and is
                // directly clickable.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Configuration app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_general_audit.menu_general_audit_configuration"]',
                },
                {
                    // Standard & Regulation may be folded into the "+"
                    // overflow dropdown. Open it only when the section is not
                    // directly visible.
                    content:
                        "Open the overflow menu if Standard & Regulation is folded",
                    trigger:
                        ".o_menu_sections > li > " +
                        '[data-menu-xmlid="ssi_general_audit.menu_configuration_std_regulation"], ' +
                        ".o_menu_sections li.o_extra_menu_items > a",
                    run: function () {
                        if (this.$anchor.closest("li").hasClass("o_extra_menu_items")) {
                            this.$anchor[0].click();
                        }
                    },
                },
                {
                    content:
                        "Open the Standard & Regulation section if it is not folded",
                    trigger:
                        ".o_menu_sections > li > " +
                        '[data-menu-xmlid="ssi_general_audit.menu_configuration_std_regulation"]' +
                        ":not(.dropdown-item), " +
                        ".o_menu_sections li.o_extra_menu_items.show > ul",
                    run: function () {
                        if (this.$anchor.is("[data-menu-xmlid]")) {
                            this.$anchor[0].click();
                        }
                    },
                },
                {
                    content: "Open the Data Collection Categories menu",
                    trigger:
                        ".o_menu_sections " +
                        "[data-menu-xmlid='ssi_general_audit_worksheet_client_package" +
                        ".general_audit_data_collection_category_menu']",
                },
                {
                    content: "The Data Collection Categories list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Data Collection Categories)",
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

                // Flow 3 - Fill in the required fields.
                {
                    content: "Fill in the Name",
                    trigger: ".o_field_widget[name='name']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text TOUR-NEW-DC-CATEGORY",
                },
                {
                    content: "Fill in the Code",
                    trigger: ".o_field_widget[name='code']",
                    run: "text /",
                },

                // Flow 4 - Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // Post-Condition - the record is really saved: the pager
                // appears and the breadcrumb is no longer "New".
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
            ]
        );
    }
);
