/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CtPurchaseOrderDashBoard } from '@ct_purchase_order/views/ct_purchase_order_dashboard';

export class CtPurchaseOrderDashBoardRenderer extends ListRenderer {};

CtPurchaseOrderDashBoardRenderer.template = 'ct_purchase_order.CtPurchaseOrderListView';
CtPurchaseOrderDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CtPurchaseOrderDashBoard})

export const CtPurchaseOrderListView = {
    ...listView,
    Renderer: CtPurchaseOrderDashBoardRenderer,
};

registry.category("views").add("ct_purchase_order_list", CtPurchaseOrderListView);
