/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmVehicleTypeDashBoard } from '@cm_vehicle_type/views/cm_vehicle_type_dashboard';

export class CmVehicleTypeDashBoardRenderer extends ListRenderer {};

CmVehicleTypeDashBoardRenderer.template = 'cm_vehicle_type.CmVehicleTypeListView';
CmVehicleTypeDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmVehicleTypeDashBoard})

export const CmVehicleTypeListView = {
    ...listView,
    Renderer: CmVehicleTypeDashBoardRenderer,
};

registry.category("views").add("cm_vehicle_type_list", CmVehicleTypeListView);
