/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmGscsTankDashBoard } from '@cm_tank_master/views/cm_gscs_tank_dashboard';

export class CmGscsTankDashBoardRenderer extends ListRenderer {};

CmGscsTankDashBoardRenderer.template = 'cm_tank_master.CmGscsTankListView';
CmGscsTankDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmGscsTankDashBoard})

export const CmGscsTankListView = {
    ...listView,
    Renderer: CmGscsTankDashBoardRenderer,
};

registry.category("views").add("cm_gscs_tank_list", CmGscsTankListView);
