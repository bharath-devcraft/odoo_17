/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmVendorMasterDashBoard } from '@cm_vendor_master/views/cm_vendor_master_dashboard';

export class CmVendorMasterDashBoardRenderer extends ListRenderer {};

CmVendorMasterDashBoardRenderer.template = 'cm_vendor_master.CmVendorMasterListView';
CmVendorMasterDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmVendorMasterDashBoard})

export const CmVendorMasterListView = {
    ...listView,
    Renderer: CmVendorMasterDashBoardRenderer,
};

registry.category("views").add("cm_vendor_master_list", CmVendorMasterListView);
