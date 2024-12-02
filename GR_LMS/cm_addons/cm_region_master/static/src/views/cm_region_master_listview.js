/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmRegionMasterDashBoard } from '@cm_region_master/views/cm_region_master_dashboard';

export class CmRegionMasterDashBoardRenderer extends ListRenderer {};

CmRegionMasterDashBoardRenderer.template = 'cm_region_master.CmRegionMasterListView';
CmRegionMasterDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmRegionMasterDashBoard})

export const CmRegionMasterListView = {
    ...listView,
    Renderer: CmRegionMasterDashBoardRenderer,
};

registry.category("views").add("cm_region_master_list", CmRegionMasterListView);
