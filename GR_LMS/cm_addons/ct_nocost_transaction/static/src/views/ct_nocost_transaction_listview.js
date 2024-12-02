/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CtNocostTransactionDashBoard } from '@ct_nocost_transaction/views/ct_nocost_transaction_dashboard';

export class CtNocostTransactionDashBoardRenderer extends ListRenderer {};

CtNocostTransactionDashBoardRenderer.template = 'ct_nocost_transaction.CtNocostTransactionListView';
CtNocostTransactionDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CtNocostTransactionDashBoard})

export const CtNocostTransactionListView = {
    ...listView,
    Renderer: CtNocostTransactionDashBoardRenderer,
};

registry.category("views").add("ct_nocost_transaction_list", CtNocostTransactionListView);
