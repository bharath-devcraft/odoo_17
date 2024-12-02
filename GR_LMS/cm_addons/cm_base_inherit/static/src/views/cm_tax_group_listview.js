/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmTaxGroupDashBoard } from '@cm_base_inherit/views/cm_tax_group_dashboard';

export class CmTaxGroupDashBoardRenderer extends ListRenderer {};

CmTaxGroupDashBoardRenderer.template = 'cm_base_inherit.CmTaxGroupListView';
CmTaxGroupDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmTaxGroupDashBoard})

export const CmTaxGroupListView = {
    ...listView,
    Renderer: CmTaxGroupDashBoardRenderer,
};

registry.category("views").add("cm_tax_group_list", CmTaxGroupListView);
