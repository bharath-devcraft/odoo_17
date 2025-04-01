/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CtPurchaseRequestDashBoard } from '@ct_purchase_request/views/ct_purchase_request_dashboard';

export class CtPurchaseRequestDashBoardRenderer extends ListRenderer {};

CtPurchaseRequestDashBoardRenderer.template = 'ct_purchase_request.CtPurchaseRequestListView';
CtPurchaseRequestDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CtPurchaseRequestDashBoard})

export const CtPurchaseRequestListView = {
    ...listView,
    Renderer: CtPurchaseRequestDashBoardRenderer,
};

registry.category("views").add("ct_purchase_request_list", CtPurchaseRequestListView);
