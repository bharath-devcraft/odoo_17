/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmVehicleMakeDashBoard } from '@cm_vehicle_make/views/cm_vehicle_make_dashboard';

export class CmVehicleMakeDashBoardRenderer extends ListRenderer {};

CmVehicleMakeDashBoardRenderer.template = 'cm_vehicle_make.CmVehicleMakeListView';
CmVehicleMakeDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmVehicleMakeDashBoard})

export const CmVehicleMakeListView = {
    ...listView,
    Renderer: CmVehicleMakeDashBoardRenderer,
};

registry.category("views").add("cm_vehicle_make_list", CmVehicleMakeListView);
