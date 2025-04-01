/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CtDeliveryChallanDashBoard } from '@ct_delivery_challan/views/ct_delivery_challan_dashboard';

export class CtDeliveryChallanDashBoardRenderer extends ListRenderer {};

CtDeliveryChallanDashBoardRenderer.template = 'ct_delivery_challan.CtDeliveryChallanListView';
CtDeliveryChallanDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CtDeliveryChallanDashBoard})

export const CtDeliveryChallanListView = {
    ...listView,
    Renderer: CtDeliveryChallanDashBoardRenderer,
};

registry.category("views").add("ct_delivery_challan_list", CtDeliveryChallanListView);
