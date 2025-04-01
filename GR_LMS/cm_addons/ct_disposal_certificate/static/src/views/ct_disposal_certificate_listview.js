/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CtDisposalCertificateDashBoard } from '@ct_disposal_certificate/views/ct_disposal_certificate_dashboard';

export class CtDisposalCertificateDashBoardRenderer extends ListRenderer {};

CtDisposalCertificateDashBoardRenderer.template = 'ct_disposal_certificate.CtDisposalCertificateListView';
CtDisposalCertificateDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CtDisposalCertificateDashBoard})

export const CtDisposalCertificateListView = {
    ...listView,
    Renderer: CtDisposalCertificateDashBoardRenderer,
};

registry.category("views").add("ct_disposal_certificate_list", CtDisposalCertificateListView);
