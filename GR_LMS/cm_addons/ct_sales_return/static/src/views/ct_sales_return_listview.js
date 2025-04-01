/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CtSalesReturnDashBoard } from '@ct_sales_return/views/ct_sales_return_dashboard';

export class CtSalesReturnDashBoardRenderer extends ListRenderer {};

CtSalesReturnDashBoardRenderer.template = 'ct_sales_return.CtSalesReturnListView';
CtSalesReturnDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CtSalesReturnDashBoard})

export const CtSalesReturnListView = {
    ...listView,
    Renderer: CtSalesReturnDashBoardRenderer,
};

registry.category("views").add("ct_sales_return_list", CtSalesReturnListView);
