/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CtQuotationSubmitDashBoard } from '@ct_quotation_submit/views/ct_quotation_submit_dashboard';

export class CtQuotationSubmitDashBoardRenderer extends ListRenderer {};

CtQuotationSubmitDashBoardRenderer.template = 'ct_quotation_submit.CtQuotationSubmitListView';
CtQuotationSubmitDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CtQuotationSubmitDashBoard})

export const CtQuotationSubmitListView = {
    ...listView,
    Renderer: CtQuotationSubmitDashBoardRenderer,
};

registry.category("views").add("ct_quotation_submit_list", CtQuotationSubmitListView);
