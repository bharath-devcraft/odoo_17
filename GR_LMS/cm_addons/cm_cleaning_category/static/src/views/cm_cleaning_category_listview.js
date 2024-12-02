/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmCleaningCategoryDashBoard } from '@cm_cleaning_category/views/cm_cleaning_category_dashboard';

export class CmCleaningCategoryDashBoardRenderer extends ListRenderer {};

CmCleaningCategoryDashBoardRenderer.template = 'cm_cleaning_category.CmCleaningCategoryListView';
CmCleaningCategoryDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmCleaningCategoryDashBoard})

export const CmCleaningCategoryListView = {
    ...listView,
    Renderer: CmCleaningCategoryDashBoardRenderer,
};

registry.category("views").add("cm_cleaning_category_list", CmCleaningCategoryListView);
