/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmCustomerBusinessActivityDashBoard } from '@cm_customer_business_activity/views/cm_customer_business_activity_dashboard';

export class CmCustomerBusinessActivityDashBoardRenderer extends ListRenderer {};

CmCustomerBusinessActivityDashBoardRenderer.template = 'cm_customer_business_activity.CmCustomerBusinessActivityListView';
CmCustomerBusinessActivityDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmCustomerBusinessActivityDashBoard})

export const CmCustomerBusinessActivityListView = {
    ...listView,
    Renderer: CmCustomerBusinessActivityDashBoardRenderer,
};

registry.category("views").add("cm_customer_business_activity_list", CmCustomerBusinessActivityListView);
