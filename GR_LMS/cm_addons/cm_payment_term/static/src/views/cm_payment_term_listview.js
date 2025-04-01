/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmPaymentTermDashBoard } from '@cm_payment_term/views/cm_payment_term_dashboard';

export class CmPaymentTermDashBoardRenderer extends ListRenderer {};

CmPaymentTermDashBoardRenderer.template = 'cm_payment_term.CmPaymentTermListView';
CmPaymentTermDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmPaymentTermDashBoard})

export const CmPaymentTermListView = {
    ...listView,
    Renderer: CmPaymentTermDashBoardRenderer,
};

registry.category("views").add("cm_payment_term_list", CmPaymentTermListView);
