/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmDepotLocationDashBoard } from '@cm_depot_location/views/cm_depot_location_dashboard';

export class CmDepotLocationDashBoardRenderer extends ListRenderer {};

CmDepotLocationDashBoardRenderer.template = 'cm_depot_location.CmDepotLocationListView';
CmDepotLocationDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmDepotLocationDashBoard})

export const CmDepotLocationListView = {
    ...listView,
    Renderer: CmDepotLocationDashBoardRenderer,
};

registry.category("views").add("cm_depot_location_list", CmDepotLocationListView);
