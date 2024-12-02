/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmProductTemplateAccessoriesDashBoard } from '@cm_product_inherit/views/cm_product_template_accessories_dashboard';

export class CmProductTemplateAccessoriesDashBoardRenderer extends ListRenderer {};

CmProductTemplateAccessoriesDashBoardRenderer.template = 'cm_product_inherit.CmProductTemplateAccessoriesListView';
CmProductTemplateAccessoriesDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmProductTemplateAccessoriesDashBoard})

export const CmProductTemplateAccessoriesListView = {
    ...listView,
    Renderer: CmProductTemplateAccessoriesDashBoardRenderer,
};

registry.category("views").add("cm_product_template_accessories_list", CmProductTemplateAccessoriesListView);
