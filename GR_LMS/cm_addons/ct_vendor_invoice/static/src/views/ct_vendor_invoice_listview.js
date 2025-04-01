/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CtVendorInvoiceDashBoard } from '@ct_vendor_invoice/views/ct_vendor_invoice_dashboard';

export class CtVendorInvoiceDashBoardRenderer extends ListRenderer {};

CtVendorInvoiceDashBoardRenderer.template = 'ct_vendor_invoice.CtVendorInvoiceListView';
CtVendorInvoiceDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CtVendorInvoiceDashBoard})

export const CtVendorInvoiceListView = {
    ...listView,
    Renderer: CtVendorInvoiceDashBoardRenderer,
};

registry.category("views").add("ct_vendor_invoice_list", CtVendorInvoiceListView);
