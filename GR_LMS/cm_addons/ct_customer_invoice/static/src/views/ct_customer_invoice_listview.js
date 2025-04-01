/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CtCustomerInvoiceDashBoard } from '@ct_customer_invoice/views/ct_customer_invoice_dashboard';

export class CtCustomerInvoiceDashBoardRenderer extends ListRenderer {};

CtCustomerInvoiceDashBoardRenderer.template = 'ct_customer_invoice.CtCustomerInvoiceListView';
CtCustomerInvoiceDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CtCustomerInvoiceDashBoard})

export const CtCustomerInvoiceListView = {
    ...listView,
    Renderer: CtCustomerInvoiceDashBoardRenderer,
};

registry.category("views").add("ct_customer_invoice_list", CtCustomerInvoiceListView);
