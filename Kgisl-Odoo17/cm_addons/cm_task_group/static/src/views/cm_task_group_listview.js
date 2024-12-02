/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmTaskGroupDashBoard } from '@cm_task_group/views/cm_task_group_dashboard';

export class CmTaskGroupDashBoardRenderer extends ListRenderer {};

CmTaskGroupDashBoardRenderer.template = 'cm_task_group.CmTaskGroupListView';
CmTaskGroupDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmTaskGroupDashBoard})

export const CmTaskGroupListView = {
    ...listView,
    Renderer: CmTaskGroupDashBoardRenderer,
};

registry.category("views").add("cm_task_group_list", CmTaskGroupListView);
