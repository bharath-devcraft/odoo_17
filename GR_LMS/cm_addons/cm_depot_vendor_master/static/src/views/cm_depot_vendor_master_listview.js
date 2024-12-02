/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmDepotVendorMasterDashBoard } from '@cm_depot_vendor_master/views/cm_depot_vendor_master_dashboard';

export class CmDepotVendorMasterDashBoardRenderer extends ListRenderer {};

CmDepotVendorMasterDashBoardRenderer.template = 'cm_depot_vendor_master.CmDepotVendorMasterListView';
CmDepotVendorMasterDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmDepotVendorMasterDashBoard})

export const CmDepotVendorMasterListView = {
    ...listView,
    Renderer: CmDepotVendorMasterDashBoardRenderer,
};

registry.category("views").add("cm_depot_vendor_master_list", CmDepotVendorMasterListView);
