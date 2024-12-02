/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CtQuotationsDashBoard } from '@ct_quotations/views/ct_quotations_dashboard';

export class CtQuotationsDashBoardRenderer extends ListRenderer {};

CtQuotationsDashBoardRenderer.template = 'ct_quotations.CtQuotationsListView';
CtQuotationsDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CtQuotationsDashBoard})

export const CtQuotationsListView = {
    ...listView,
    Renderer: CtQuotationsDashBoardRenderer,
};

registry.category("views").add("ct_quotations_list", CtQuotationsListView);
