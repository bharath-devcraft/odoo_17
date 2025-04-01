/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CtQuotationComparisonDashBoard } from '@ct_quotation_comparison/views/ct_quotation_comparison_dashboard';

export class CtQuotationComparisonDashBoardRenderer extends ListRenderer {};

CtQuotationComparisonDashBoardRenderer.template = 'ct_quotation_comparison.CtQuotationComparisonListView';
CtQuotationComparisonDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CtQuotationComparisonDashBoard})

export const CtQuotationComparisonListView = {
    ...listView,
    Renderer: CtQuotationComparisonDashBoardRenderer,
};

registry.category("views").add("ct_quotation_comparison_list", CtQuotationComparisonListView);
