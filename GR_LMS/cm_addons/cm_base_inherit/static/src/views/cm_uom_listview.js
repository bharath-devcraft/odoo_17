/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmUomDashBoard } from '@cm_base_inherit/views/cm_uom_dashboard';

export class CmUomDashBoardRenderer extends ListRenderer {};

CmUomDashBoardRenderer.template = 'cm_base_inherit.CmUomListView';
CmUomDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmUomDashBoard})

export const CmUomListView = {
    ...listView,
    Renderer: CmUomDashBoardRenderer,
};

registry.category("views").add("cm_uom_list", CmUomListView);
