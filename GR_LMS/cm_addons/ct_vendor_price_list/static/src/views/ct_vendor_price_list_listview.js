/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CtVendorPriceListDashBoard } from '@ct_vendor_price_list/views/ct_vendor_price_list_dashboard';

export class CtVendorPriceListDashBoardRenderer extends ListRenderer {};

CtVendorPriceListDashBoardRenderer.template = 'ct_vendor_price_list.CtVendorPriceListListView';
CtVendorPriceListDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CtVendorPriceListDashBoard})

export const CtVendorPriceListListView = {
    ...listView,
    Renderer: CtVendorPriceListDashBoardRenderer,
};

registry.category("views").add("ct_vendor_price_list_view", CtVendorPriceListListView);
