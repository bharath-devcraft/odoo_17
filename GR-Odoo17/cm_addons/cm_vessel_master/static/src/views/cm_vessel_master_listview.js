/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmVesselMasterDashBoard } from '@cm_vessel_master/views/cm_vessel_master_dashboard';

export class CmVesselMasterDashBoardRenderer extends ListRenderer {};

CmVesselMasterDashBoardRenderer.template = 'cm_vessel_master.CmVesselMasterListView';
CmVesselMasterDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmVesselMasterDashBoard})

export const CmVesselMasterListView = {
    ...listView,
    Renderer: CmVesselMasterDashBoardRenderer,
};

registry.category("views").add("cm_vessel_master_list", CmVesselMasterListView);
