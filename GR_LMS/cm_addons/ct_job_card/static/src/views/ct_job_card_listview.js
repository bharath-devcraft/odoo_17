/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CtJobCardDashBoard } from '@ct_job_card/views/ct_job_card_dashboard';

export class CtJobCardDashBoardRenderer extends ListRenderer {};

CtJobCardDashBoardRenderer.template = 'ct_job_card.CtJobCardListView';
CtJobCardDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CtJobCardDashBoard})

export const CtJobCardListView = {
    ...listView,
    Renderer: CtJobCardDashBoardRenderer,
};

registry.category("views").add("ct_job_card_list", CtJobCardListView);
