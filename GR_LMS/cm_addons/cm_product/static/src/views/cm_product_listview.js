/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmProductDashBoard } from '@cm_product/views/cm_product_dashboard';

export class CmProductDashBoardRenderer extends ListRenderer {};

CmProductDashBoardRenderer.template = 'cm_product.CmProductListView';
CmProductDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmProductDashBoard})

export const CmProductListView = {
    ...listView,
    Renderer: CmProductDashBoardRenderer,
};

registry.category("views").add("cm_product_list", CmProductListView);
