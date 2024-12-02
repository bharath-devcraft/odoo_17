/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmProductCategoryDashBoard } from '@cm_base_inherit/views/cm_product_category_dashboard';

export class CmProductCategoryDashBoardRenderer extends ListRenderer {};

CmProductCategoryDashBoardRenderer.template = 'cm_base_inherit.CmProductCategoryListView';
CmProductCategoryDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmProductCategoryDashBoard})

export const CmProductCategoryListView = {
    ...listView,
    Renderer: CmProductCategoryDashBoardRenderer,
};

registry.category("views").add("cm_product_category_list", CmProductCategoryListView);
