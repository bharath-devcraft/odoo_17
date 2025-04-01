/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CtBusinessConfirmationDashBoard } from '@ct_business_confirmation/views/ct_business_confirmation_dashboard';

export class CtBusinessConfirmationDashBoardRenderer extends ListRenderer {};

CtBusinessConfirmationDashBoardRenderer.template = 'ct_business_confirmation.CtBusinessConfirmationListView';
CtBusinessConfirmationDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CtBusinessConfirmationDashBoard})

export const CtBusinessConfirmationListView = {
    ...listView,
    Renderer: CtBusinessConfirmationDashBoardRenderer,
};

registry.category("views").add("ct_business_confirmation_list", CtBusinessConfirmationListView);
