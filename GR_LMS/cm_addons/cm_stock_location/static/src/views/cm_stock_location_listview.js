/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmStockLocationDashBoard } from '@cm_stock_location/views/cm_stock_location_dashboard';

export class CmStockLocationDashBoardRenderer extends ListRenderer {};

CmStockLocationDashBoardRenderer.template = 'cm_stock_location.CmStockLocationListView';
CmStockLocationDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmStockLocationDashBoard})

export const CmStockLocationListView = {
    ...listView,
    Renderer: CmStockLocationDashBoardRenderer,
};

registry.category("views").add("cm_stock_location_list", CmStockLocationListView);
