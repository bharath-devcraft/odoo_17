/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CtRfqDashBoard } from '@ct_rfq/views/ct_rfq_dashboard';

export class CtRfqDashBoardRenderer extends ListRenderer {};

CtRfqDashBoardRenderer.template = 'ct_rfq.CtRfqListView';
CtRfqDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CtRfqDashBoard})

export const CtRfqListView = {
    ...listView,
    Renderer: CtRfqDashBoardRenderer,
};

registry.category("views").add("ct_rfq_list", CtRfqListView);
