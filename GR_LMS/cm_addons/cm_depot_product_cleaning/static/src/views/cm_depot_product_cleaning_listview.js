/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmDepotProductCleaningDashBoard } from '@cm_depot_product_cleaning/views/cm_depot_product_cleaning_dashboard';

export class CmDepotProductCleaningDashBoardRenderer extends ListRenderer {};

CmDepotProductCleaningDashBoardRenderer.template = 'cm_depot_product_cleaning.CmDepotProductCleaningListView';
CmDepotProductCleaningDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmDepotProductCleaningDashBoard})

export const CmDepotProductCleaningListView = {
    ...listView,
    Renderer: CmDepotProductCleaningDashBoardRenderer,
};

registry.category("views").add("cm_depot_product_cleaning_list", CmDepotProductCleaningListView);
