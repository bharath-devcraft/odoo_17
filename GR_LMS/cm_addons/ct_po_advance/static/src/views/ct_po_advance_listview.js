/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CtPoAdvanceDashBoard } from '@ct_po_advance/views/ct_po_advance_dashboard';

export class CtPoAdvanceDashBoardRenderer extends ListRenderer {};

CtPoAdvanceDashBoardRenderer.template = 'ct_po_advance.CtPoAdvanceListView';
CtPoAdvanceDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CtPoAdvanceDashBoard})

export const CtPoAdvanceListView = {
    ...listView,
    Renderer: CtPoAdvanceDashBoardRenderer,
};

registry.category("views").add("ct_po_advance_list", CtPoAdvanceListView);
