/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmTransportVendorDashBoard } from '@cm_transport_vendor/views/cm_transport_vendor_dashboard';

export class CmTransportVendorDashBoardRenderer extends ListRenderer {};

CmTransportVendorDashBoardRenderer.template = 'cm_transport_vendor.CmTransportVendorListView';
CmTransportVendorDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmTransportVendorDashBoard})

export const CmTransportVendorListView = {
    ...listView,
    Renderer: CmTransportVendorDashBoardRenderer,
};

registry.category("views").add("cm_transport_vendor_list", CmTransportVendorListView);
