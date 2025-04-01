/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmRepairCodeDashBoard } from '@cm_repair_code/views/cm_repair_code_dashboard';

export class CmRepairCodeDashBoardRenderer extends ListRenderer {};

CmRepairCodeDashBoardRenderer.template = 'cm_repair_code.CmRepairCodeListView';
CmRepairCodeDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmRepairCodeDashBoard})

export const CmRepairCodeListView = {
    ...listView,
    Renderer: CmRepairCodeDashBoardRenderer,
};

registry.category("views").add("cm_repair_code_list", CmRepairCodeListView);
