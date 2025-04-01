/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmSocTankDashBoard } from '@cm_tank_master/views/cm_soc_tank_dashboard';

export class CmSocTankDashBoardRenderer extends ListRenderer {};

CmSocTankDashBoardRenderer.template = 'cm_tank_master.CmSocTankListView';
CmSocTankDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmSocTankDashBoard})

export const CmSocTankListView = {
    ...listView,
    Renderer: CmSocTankDashBoardRenderer,
};

registry.category("views").add("cm_soc_tank_list", CmSocTankListView);
