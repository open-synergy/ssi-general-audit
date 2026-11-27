/* Copyright 2026 OpenSynergy Indonesia
 Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html). */

odoo.define(
    "ssi_general_audit_worksheet_client_package.general_audit_ws_f5a3cee_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/general_audit_ws_f5a3cee/01-create.md
        tour.register(
            "ssi_general_audit_worksheet_client_package_f5a3cee_create",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 - Open the Risk Assessment > Client Assistance Package > Data Collection menu.
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
                    content: "Open the Data Collection menu",
                    trigger:
                        ".o_menu_sections " +
                        "[data-menu-xmlid='ssi_general_audit_worksheet_client_package" +
                        ".general_audit_ws_f5a3cee_menu']",
                },
                {
                    content: "The worksheet list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Data Collection)",
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
                    run: "text TOUR-F5A3CEE-GA",
                },
                {
                    content: "Pick the General Audit from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR-F5A3CEE-GA)",
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

        // IK: docs/general_audit_ws_f5a3cee/02-populate-details.md
        tour.register(
            "ssi_general_audit_worksheet_client_package_f5a3cee_populate_details",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 - Open the Risk Assessment > Client Assistance Package > Data Collection menu.
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
                    content: "Open the Data Collection menu",
                    trigger:
                        ".o_menu_sections " +
                        "[data-menu-xmlid='ssi_general_audit_worksheet_client_package" +
                        ".general_audit_ws_f5a3cee_menu']",
                },
                {
                    content: "The worksheet list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Data Collection)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 2 - Open the worksheet to work on.
                {
                    content: "Open the worksheet",
                    trigger:
                        ".o_list_view .o_data_row:contains(TOUR-F5A3CEE-POPULATE) " +
                        ".o_data_cell:first",
                },
                {
                    content: "Status is On Progress",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='open'].btn-primary",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 3 - Click the Populate button above the tabs.
                {
                    content: "Click Populate",
                    trigger: "button[name='action_populate_details']",
                },

                // Flow 4 - Open the Details tab. The tabs are Primary,
                // Permanent/Current and Details, in that order.
                {
                    content:
                        "The first tabs are Primary, Permanent/Current and Details",
                    trigger:
                        ".o_notebook .nav-tabs li:first-child:contains(Primary)" +
                        " + li:contains(Permanent/Current) + li:contains(Details) a",
                },

                // Flow 5 - Click a line in Details to review its data.
                {
                    content: "Open the populated account type",
                    trigger:
                        ".tab-pane.active .o_field_widget[name='detail_ids'] " +
                        ".o_data_row:contains(TOUR-F5A3CEE-POPULATE) .o_data_cell:first",
                },
                {
                    content: "The data line of the account type is displayed",
                    // 14.0 searches inside the open dialog, so the trigger
                    // must not be prefixed with ".modal".
                    trigger:
                        ".o_field_widget[name='line_ids'] " +
                        ".o_data_row:contains(Tour account item)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Close the Details line",
                    trigger: ".modal-header button.close",
                },

                // Flow 7 - Open the Permanent/Current tab.
                {
                    content: "Open the Permanent/Current tab",
                    trigger: ".o_notebook .nav-tabs a:contains(Permanent/Current)",
                    extra_trigger: "body:not(.modal-open)",
                },

                // Post-Condition - the Permanent File and Current File items
                // are listed apart.
                {
                    content: "The Permanent File item is listed in Permanent File",
                    trigger:
                        ".tab-pane.active .o_field_widget[name='permanent_ids'] " +
                        ".o_data_row:contains(Tour permanent item)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "The Current File list does not hold it",
                    trigger:
                        ".tab-pane.active .o_field_widget[name='current_ids']" +
                        ":not(:has(.o_data_row:contains(Tour permanent item)))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 8 - Open the Primary tab.
                {
                    content: "Open the Primary tab",
                    trigger: ".o_notebook .nav-tabs a:contains(Primary)",
                },

                // Post-Condition - Client Assistance Package holds the
                // populated Primary items, above the reporting timetable.
                {
                    content: "The Primary item is listed",
                    trigger:
                        ".tab-pane.active .o_field_widget[name='primary_ids'] " +
                        ".o_data_row:contains(Tour primary item)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Client Assistance Package is above the timetable",
                    trigger:
                        ".tab-pane.active " +
                        ".o_inner_group:has(.o_field_widget[name='primary_ids'])" +
                        " ~ .o_inner_group " +
                        ".o_field_widget[name='reporting_timetable_ids']",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Post-Condition - Populate does not fill the reporting
                // timetable.
                {
                    content: "The reporting timetable is displayed without lines",
                    trigger:
                        ".tab-pane.active " +
                        ".o_field_widget[name='reporting_timetable_ids']" +
                        ":not(:has(.o_data_row))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );
    }
);
