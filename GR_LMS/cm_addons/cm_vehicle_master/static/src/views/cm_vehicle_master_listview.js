/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmVehicleMasterDashBoard } from '@cm_vehicle_master/views/cm_vehicle_master_dashboard';

export class CmVehicleMasterDashBoardRenderer extends ListRenderer {};

CmVehicleMasterDashBoardRenderer.template = 'cm_vehicle_master.CmVehicleMasterListView';
CmVehicleMasterDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmVehicleMasterDashBoard})

export const CmVehicleMasterListView = {
    ...listView,
    Renderer: CmVehicleMasterDashBoardRenderer,
};

registry.category("views").add("cm_vehicle_master_list", CmVehicleMasterListView);
