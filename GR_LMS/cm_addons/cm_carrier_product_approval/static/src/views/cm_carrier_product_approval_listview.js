/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmCarrierProductApprovalDashBoard } from '@cm_carrier_product_approval/views/cm_carrier_product_approval_dashboard';

export class CmCarrierProductApprovalDashBoardRenderer extends ListRenderer {};

CmCarrierProductApprovalDashBoardRenderer.template = 'cm_carrier_product_approval.CmCarrierProductApprovalListView';
CmCarrierProductApprovalDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmCarrierProductApprovalDashBoard})

export const CmCarrierProductApprovalListView = {
    ...listView,
    Renderer: CmCarrierProductApprovalDashBoardRenderer,
};

registry.category("views").add("cm_carrier_product_approval_list", CmCarrierProductApprovalListView);
