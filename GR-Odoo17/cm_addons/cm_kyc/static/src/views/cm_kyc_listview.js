/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmKycDashBoard } from '@cm_kyc/views/cm_kyc_dashboard';

export class CmKycDashBoardRenderer extends ListRenderer {};

CmKycDashBoardRenderer.template = 'cm_kyc.CmKYCListView';
CmKycDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmKycDashBoard})

export const CmKYCListView = {
    ...listView,
    Renderer: CmKycDashBoardRenderer,
};

registry.category("views").add("cm_kyc_list", CmKYCListView);
