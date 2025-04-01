/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmOtOpTankDashBoard } from '@cm_tank_master/views/cm_ot_op_tank_dashboard';

export class CmOtOpTankDashBoardRenderer extends ListRenderer {};

CmOtOpTankDashBoardRenderer.template = 'cm_tank_master.CmOtOpTankListView';
CmOtOpTankDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmOtOpTankDashBoard})

export const CmOtOpTankListView = {
    ...listView,
    Renderer: CmOtOpTankDashBoardRenderer,
};

registry.category("views").add("cm_ot_op_tank_list", CmOtOpTankListView);
