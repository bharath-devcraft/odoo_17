/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CtSalesLeadDashBoard } from '@ct_sales_lead/views/ct_sales_lead_dashboard';

export class CtSalesLeadDashBoardRenderer extends ListRenderer {};

CtSalesLeadDashBoardRenderer.template = 'ct_sales_lead.CtSalesLeadListView';
CtSalesLeadDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CtSalesLeadDashBoard})

export const CtSalesLeadListView = {
    ...listView,
    Renderer: CtSalesLeadDashBoardRenderer,
};

registry.category("views").add("ct_sales_lead_list", CtSalesLeadListView);
