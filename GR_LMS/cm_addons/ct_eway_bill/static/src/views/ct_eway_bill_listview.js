/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CtEwayBillDashBoard } from '@ct_eway_bill/views/ct_eway_bill_dashboard';

export class CtEwayBillDashBoardRenderer extends ListRenderer {};

CtEwayBillDashBoardRenderer.template = 'ct_eway_bill.CtEwayBillListView';
CtEwayBillDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CtEwayBillDashBoard})

export const CtEwayBillListView = {
    ...listView,
    Renderer: CtEwayBillDashBoardRenderer,
};

registry.category("views").add("ct_eway_bill_list", CtEwayBillListView);
