/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmVendorTypeDashBoard } from '@cm_vendor_type/views/cm_vendor_type_dashboard';

export class CmVendorTypeDashBoardRenderer extends ListRenderer {};

CmVendorTypeDashBoardRenderer.template = 'cm_vendor_type.CmVendorTypeListView';
CmVendorTypeDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmVendorTypeDashBoard})

export const CmVendorTypeListView = {
    ...listView,
    Renderer: CmVendorTypeDashBoardRenderer,
};

registry.category("views").add("cm_vendor_type_list", CmVendorTypeListView);
