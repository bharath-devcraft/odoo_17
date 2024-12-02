/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmTransportLocationDashBoard } from '@cm_transport_location/views/cm_transport_location_dashboard';

export class CmTransportLocationDashBoardRenderer extends ListRenderer {};

CmTransportLocationDashBoardRenderer.template = 'cm_transport_location.CmTransportLocationListView';
CmTransportLocationDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmTransportLocationDashBoard})

export const CmTransportLocationListView = {
    ...listView,
    Renderer: CmTransportLocationDashBoardRenderer,
};

registry.category("views").add("cm_transport_location_list", CmTransportLocationListView);
