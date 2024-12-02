/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmEnquirySourceDashBoard } from '@cm_enquiry_source/views/cm_enquiry_source_dashboard';

export class CmEnquirySourceDashBoardRenderer extends ListRenderer {};

CmEnquirySourceDashBoardRenderer.template = 'cm_enquiry_source.CmEnquirySourceListView';
CmEnquirySourceDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmEnquirySourceDashBoard})

export const CmEnquirySourceListView = {
    ...listView,
    Renderer: CmEnquirySourceDashBoardRenderer,
};

registry.category("views").add("cm_enquiry_source_list", CmEnquirySourceListView);
