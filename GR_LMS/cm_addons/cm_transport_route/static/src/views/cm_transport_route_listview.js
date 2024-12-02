/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmTransportRouteDashBoard } from '@cm_transport_route/views/cm_transport_route_dashboard';

export class CmTransportRouteDashBoardRenderer extends ListRenderer {};

CmTransportRouteDashBoardRenderer.template = 'cm_transport_route.CmTransportRouteListView';
CmTransportRouteDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmTransportRouteDashBoard})

export const CmTransportRouteListView = {
    ...listView,
    Renderer: CmTransportRouteDashBoardRenderer,
};

registry.category("views").add("cm_transport_route_list", CmTransportRouteListView);
