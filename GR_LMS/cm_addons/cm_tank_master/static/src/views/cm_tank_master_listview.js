/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmTankMasterDashBoard } from '@cm_tank_master/views/cm_tank_master_dashboard';

export class CmTankMasterDashBoardRenderer extends ListRenderer {};

CmTankMasterDashBoardRenderer.template = 'cm_tank_master.CmTankMasterListView';
CmTankMasterDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmTankMasterDashBoard})

export const CmTankMasterListView = {
    ...listView,
    Renderer: CmTankMasterDashBoardRenderer,
};

registry.category("views").add("cm_tank_master_list", CmTankMasterListView);
