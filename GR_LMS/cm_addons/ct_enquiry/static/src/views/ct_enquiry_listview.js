/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CtEnquiryDashBoard } from '@ct_enquiry/views/ct_enquiry_dashboard';

export class CtEnquiryDashBoardRenderer extends ListRenderer {};

CtEnquiryDashBoardRenderer.template = 'ct_enquiry.CtEnquiryListView';
CtEnquiryDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CtEnquiryDashBoard})

export const CtEnquiryListView = {
    ...listView,
    Renderer: CtEnquiryDashBoardRenderer,
};

registry.category("views").add("ct_enquiry_list", CtEnquiryListView);
