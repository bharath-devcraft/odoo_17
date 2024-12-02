/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmSupplierDashBoard } from '@cm_supplier_customer/views/cm_supplier_dashboard';

export class CmSupplierDashBoardRenderer extends ListRenderer {};

CmSupplierDashBoardRenderer.template = 'cm_supplier_customer.CmSupplierListView';
CmSupplierDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmSupplierDashBoard})

export const CmSupplierListView = {
    ...listView,
    Renderer: CmSupplierDashBoardRenderer,
};

registry.category("views").add("cm_supplier_list", CmSupplierListView);
