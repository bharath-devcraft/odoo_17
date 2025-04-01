/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CtDomsBusinessConfirmationDashBoard } from '@ct_doms_business_confirmation/views/ct_doms_business_confirmation_dashboard';

export class CtDomsBusinessConfirmationDashBoardRenderer extends ListRenderer {};

CtDomsBusinessConfirmationDashBoardRenderer.template = 'ct_doms_business_confirmation.CtDomsBusinessConfirmationListView';
CtDomsBusinessConfirmationDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CtDomsBusinessConfirmationDashBoard})

export const CtDomsBusinessConfirmationListView = {
    ...listView,
    Renderer: CtDomsBusinessConfirmationDashBoardRenderer,
};

registry.category("views").add("ct_doms_business_confirmation_list", CtDomsBusinessConfirmationListView);
