/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmSdsProductDashBoard } from '@cm_sds_product/views/cm_sds_product_dashboard';

export class CmSdsProductDashBoardRenderer extends ListRenderer {};

CmSdsProductDashBoardRenderer.template = 'cm_sds_product.CmSdsProductListView';
CmSdsProductDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmSdsProductDashBoard})

export const CmSdsProductListView = {
    ...listView,
    Renderer: CmSdsProductDashBoardRenderer,
};

registry.category("views").add("cm_sds_product_list", CmSdsProductListView);
