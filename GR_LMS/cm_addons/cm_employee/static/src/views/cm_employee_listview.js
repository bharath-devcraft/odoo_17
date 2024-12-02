/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmEmployeeDashBoard } from '@cm_employee/views/cm_employee_dashboard';

export class CmEmployeeDashBoardRenderer extends ListRenderer {};

CmEmployeeDashBoardRenderer.template = 'cm_employee.CmEmployeeListView';
CmEmployeeDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmEmployeeDashBoard})

export const CmEmployeeListView = {
    ...listView,
    Renderer: CmEmployeeDashBoardRenderer,
};

registry.category("views").add("cm_employee_list", CmEmployeeListView);
