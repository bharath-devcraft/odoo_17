/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmKycMasterDashBoard } from '@cm_kyc_master/views/cm_kyc_master_dashboard';

export class CmKycMasterDashBoardRenderer extends ListRenderer {};

CmKycMasterDashBoardRenderer.template = 'cm_kyc_master.CmKycMasterListView';
CmKycMasterDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmKycMasterDashBoard})

export const CmKycMasterListView = {
    ...listView,
    Renderer: CmKycMasterDashBoardRenderer,
};

registry.category("views").add("cm_kyc_master_list", CmKycMasterListView);
