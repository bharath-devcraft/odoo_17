/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmVesselServiceRouteDashBoard } from '@cm_vessel_service_route/views/cm_vessel_service_route_dashboard';

export class CmVesselServiceRouteDashBoardRenderer extends ListRenderer {};

CmVesselServiceRouteDashBoardRenderer.template = 'cm_vessel_service_route.CmVesselServiceRouteListView';
CmVesselServiceRouteDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmVesselServiceRouteDashBoard})

export const CmVesselServiceRouteListView = {
    ...listView,
    Renderer: CmVesselServiceRouteDashBoardRenderer,
};

registry.category("views").add("cm_vessel_service_route_list", CmVesselServiceRouteListView);
