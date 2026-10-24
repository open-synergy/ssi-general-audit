/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html). */

odoo.define("ssi_general_audit_import_template.import_template_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // Flow 1 of every tour below: open Configuration > Import Templates.
    // The menu is a level-1 leaf of the Configuration app, so one step opens
    // the app and one step opens the menu.
    var openMenu = [
        tour.stepUtils.showAppsMenuItem(),
        {
            content: "Open the Configuration app",
            trigger:
                '.o_app[data-menu-xmlid="ssi_general_audit.menu_general_audit_configuration"]',
        },
        {
            // The Configuration app has more level-1 sections than fit the
            // 1366px navbar, so the last leaf (sequence 300) is folded into
            // the "+" overflow dropdown. Open it when the leaf is not
            // directly visible; otherwise the leaf itself matches first.
            content: "Open the overflow menu if the leaf is folded",
            trigger:
                '.o_menu_sections > li > [data-menu-xmlid="ssi_general_audit_import_template.general_audit_import_template_menu"], .o_menu_sections li.o_extra_menu_items > a',
        },
        {
            content: "Open the Import Templates menu",
            trigger:
                '.o_menu_sections [data-menu-xmlid="ssi_general_audit_import_template.general_audit_import_template_menu"]',
        },
        {
            // Gate: the title of the target action. ".o_list_view" alone
            // would also match the app's landing list.
            content: "Import Templates list is displayed",
            trigger:
                ".o_control_panel .breadcrumb-item.active:contains(Import Templates)",
            extra_trigger: ".o_list_view",
            run: function () {
                // Assertion only; do not trigger the default click action.
            },
        },
    ];

    // IK: docs/general_audit_import_template/01-create.md
    tour.register(
        "ssi_general_audit_import_template_create",
        {
            test: true,
            url: "/web",
        },
        openMenu.concat([
            // Flow 2 - Click the New button ("Create" in 14.0)
            {
                content: "Click Create",
                trigger: ".o_list_button_add",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open in edit mode",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // Flow 3 - Fill in the Name
            {
                content: "Fill in the Name",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-NEW-TEMPLATE",
            },

            // Flow 4 - Settings tab: Target Model.
            {
                content: "Open the Settings tab",
                trigger: ".o_notebook .nav-link:contains(Settings)",
                extra_trigger: ".o_form_view.o_form_editable",
            },
            {
                content: "Select the Target Model",
                trigger: ".o_field_many2one[name='model_id'] input",
                extra_trigger: ".o_notebook .nav-link.active:contains(Settings)",
                run: "text Client Business Cycle",
            },
            {
                content: "Pick the Target Model from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(Client Business Cycle)",
            },

            // Flow 5 - Columns tab: add one column
            {
                content: "Open the Columns tab",
                trigger: ".o_notebook .nav-link:contains(Columns)",
                extra_trigger: ".o_form_view.o_form_editable",
            },
            {
                content: "Add a line",
                trigger: ".tab-pane.active .o_field_x2many_list_row_add a",
                extra_trigger: ".o_notebook .nav-link.active:contains(Columns)",
            },
            {
                content: "Fill in the Column Title",
                trigger: ".o_selected_row .o_field_widget[name='name']",
                run: "text TOUR-COLUMN-TITLE",
            },

            // Flow 6 - Click Save
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // Post-Condition - the column is listed on the Columns tab.
            {
                content: "The column is listed on the Columns tab",
                trigger:
                    ".o_field_widget[name='line_ids'] " +
                    ".o_data_row:contains(TOUR-COLUMN-TITLE)",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ])
    );

    // IK: docs/general_audit_import_template/02-create-server-action.md
    tour.register(
        "ssi_general_audit_import_template_create_server_action",
        {
            test: true,
            url: "/web",
        },
        openMenu.concat([
            // Flow 2 - Open the template
            {
                content: "Open the template",
                trigger: ".o_data_row:contains(TOUR-IMPORT-TEMPLATE)",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open with the Create Server Action button",
                trigger: ".o_form_statusbar button[name='action_create_server_action']",
                extra_trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // Flow 3 - Click Create Server Action
            {
                content: "Click Create Server Action",
                trigger: ".o_form_statusbar button[name='action_create_server_action']",
            },

            // Post-Condition - the Remove Server Action button replaces it.
            {
                content: "Remove Server Action button is displayed",
                trigger: ".o_form_statusbar button[name='action_remove_server_action']",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ])
    );
});
