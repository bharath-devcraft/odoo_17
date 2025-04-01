/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmProductManufacturerDashBoard } from '@cm_product_manufacturer/views/cm_product_manufacturer_dashboard';

export class CmProductManufacturerDashBoardRenderer extends ListRenderer {};

CmProductManufacturerDashBoardRenderer.template = 'cm_product_manufacturer.CmProductManufacturerListView';
CmProductManufacturerDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmProductManufacturerDashBoard})

export const CmProductManufacturerListView = {
    ...listView,
    Renderer: CmProductManufacturerDashBoardRenderer,
};

registry.category("views").add("cm_product_manufacturer_list", CmProductManufacturerListView);
