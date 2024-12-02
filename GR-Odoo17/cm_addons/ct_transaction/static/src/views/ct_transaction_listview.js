/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CtTransactionDashBoard } from '@ct_transaction/views/ct_transaction_dashboard';

export class CtTransactionDashBoardRenderer extends ListRenderer {};

CtTransactionDashBoardRenderer.template = 'ct_transaction.CtTransactionListView';
CtTransactionDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CtTransactionDashBoard})

export const CtTransactionListView = {
    ...listView,
    Renderer: CtTransactionDashBoardRenderer,
};

registry.category("views").add("ct_transaction_list", CtTransactionListView);
