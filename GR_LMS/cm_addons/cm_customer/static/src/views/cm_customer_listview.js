/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmCustomerDashBoard } from '@cm_customer/views/cm_customer_dashboard';

export class CmCustomerDashBoardRenderer extends ListRenderer {};

CmCustomerDashBoardRenderer.template = 'cm_customer.CmCustomerListView';
CmCustomerDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmCustomerDashBoard})

export const CmCustomerListView = {
    ...listView,
    Renderer: CmCustomerDashBoardRenderer,
};

registry.category("views").add("cm_customer_list", CmCustomerListView);
