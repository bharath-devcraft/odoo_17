/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmProductTemplateDashBoard } from '@cm_product_inherit/views/cm_product_template_dashboard';

export class CmProductTemplateDashBoardRenderer extends ListRenderer {};

CmProductTemplateDashBoardRenderer.template = 'cm_product_inherit.CmProductTemplateListView';
CmProductTemplateDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmProductTemplateDashBoard})

export const CmProductTemplateListView = {
    ...listView,
    Renderer: CmProductTemplateDashBoardRenderer,
};

registry.category("views").add("cm_product_template_list", CmProductTemplateListView);
