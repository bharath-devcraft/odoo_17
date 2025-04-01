/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CtPaymentVoucherDashBoard } from '@ct_payment_voucher/views/ct_payment_voucher_dashboard';

export class CtPaymentVoucherDashBoardRenderer extends ListRenderer {};

CtPaymentVoucherDashBoardRenderer.template = 'ct_payment_voucher.CtPaymentVoucherListView';
CtPaymentVoucherDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CtPaymentVoucherDashBoard})

export const CtPaymentVoucherListView = {
    ...listView,
    Renderer: CtPaymentVoucherDashBoardRenderer,
};

registry.category("views").add("ct_payment_voucher_list", CtPaymentVoucherListView);
