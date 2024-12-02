/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmContainerCategoryDashBoard } from '@cm_container_category/views/cm_container_category_dashboard';

export class CmContainerCategoryDashBoardRenderer extends ListRenderer {};

CmContainerCategoryDashBoardRenderer.template = 'cm_container_category.CmContainerCategoryListView';
CmContainerCategoryDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmContainerCategoryDashBoard})

export const CmContainerCategoryListView = {
    ...listView,
    Renderer: CmContainerCategoryDashBoardRenderer,
};

registry.category("views").add("cm_container_category_list", CmContainerCategoryListView);
