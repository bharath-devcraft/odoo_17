/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmCustomerTypeDashBoard } from '@cm_customer_type/views/cm_customer_type_dashboard';

export class CmCustomerTypeDashBoardRenderer extends ListRenderer {};

CmCustomerTypeDashBoardRenderer.template = 'cm_customer_type.CmCustomerTypeListView';
CmCustomerTypeDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmCustomerTypeDashBoard})

export const CmCustomerTypeListView = {
    ...listView,
    Renderer: CmCustomerTypeDashBoardRenderer,
};

registry.category("views").add("cm_customer_type_list", CmCustomerTypeListView);
