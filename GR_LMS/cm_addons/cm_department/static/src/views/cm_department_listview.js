/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmDepartmentDashBoard } from '@cm_department/views/cm_department_dashboard';

export class CmDepartmentDashBoardRenderer extends ListRenderer {};

CmDepartmentDashBoardRenderer.template = 'cm_department.CmDepartmentListView';
CmDepartmentDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmDepartmentDashBoard})

export const CmDepartmentListView = {
    ...listView,
    Renderer: CmDepartmentDashBoardRenderer,
};

registry.category("views").add("cm_department_list", CmDepartmentListView);
