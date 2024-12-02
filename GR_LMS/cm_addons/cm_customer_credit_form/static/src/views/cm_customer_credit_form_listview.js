/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmCustomerCreditFormDashBoard } from '@cm_customer_credit_form/views/cm_customer_credit_form_dashboard';

export class CmCustomerCreditFormDashBoardRenderer extends ListRenderer {};

CmCustomerCreditFormDashBoardRenderer.template = 'cm_customer_credit_form.CmCustomerCreditFormListView';
CmCustomerCreditFormDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmCustomerCreditFormDashBoard})

export const CmCustomerCreditFormListView = {
    ...listView,
    Renderer: CmCustomerCreditFormDashBoardRenderer,
};

registry.category("views").add("cm_customer_credit_form_list", CmCustomerCreditFormListView);
