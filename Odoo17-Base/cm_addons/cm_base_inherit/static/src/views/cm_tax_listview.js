/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmTaxDashBoard } from '@cm_base_inherit/views/cm_tax_dashboard';

export class CmTaxDashBoardRenderer extends ListRenderer {};

CmTaxDashBoardRenderer.template = 'cm_base_inherit.CmTaxListView';
CmTaxDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmTaxDashBoard})

export const CmTaxListView = {
    ...listView,
    Renderer: CmTaxDashBoardRenderer,
};

registry.category("views").add("cm_tax_list", CmTaxListView);
