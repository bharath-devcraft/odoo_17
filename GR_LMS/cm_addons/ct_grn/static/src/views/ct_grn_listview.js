/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CtGRNDashBoard } from '@ct_grn/views/ct_grn_dashboard';

export class CtGRNDashBoardRenderer extends ListRenderer {};

CtGRNDashBoardRenderer.template = 'ct_grn.CtGRNListView';
CtGRNDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CtGRNDashBoard})

export const CtGRNListView = {
    ...listView,
    Renderer: CtGRNDashBoardRenderer,
};

registry.category("views").add("ct_grn_list", CtGRNListView);
