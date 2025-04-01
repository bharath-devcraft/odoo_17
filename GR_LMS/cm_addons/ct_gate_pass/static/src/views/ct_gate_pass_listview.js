/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CtGatePassDashBoard } from '@ct_gate_pass/views/ct_gate_pass_dashboard';

export class CtGatePassDashBoardRenderer extends ListRenderer {};

CtGatePassDashBoardRenderer.template = 'ct_gate_pass.CtGatePassListView';
CtGatePassDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CtGatePassDashBoard})

export const CtGatePassListView = {
    ...listView,
    Renderer: CtGatePassDashBoardRenderer,
};

registry.category("views").add("ct_gate_pass_list", CtGatePassListView);
