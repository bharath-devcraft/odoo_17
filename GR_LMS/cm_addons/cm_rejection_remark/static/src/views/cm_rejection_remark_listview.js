/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmRejectionRemarkDashBoard } from '@cm_rejection_remark/views/cm_rejection_remark_dashboard';

export class CmRejectionRemarkDashBoardRenderer extends ListRenderer {};

CmRejectionRemarkDashBoardRenderer.template = 'cm_rejection_remark.CmRejectionRemarkListView';
CmRejectionRemarkDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmRejectionRemarkDashBoard})

export const CmRejectionRemarkListView = {
    ...listView,
    Renderer: CmRejectionRemarkDashBoardRenderer,
};

registry.category("views").add("cm_rejection_remark_list", CmRejectionRemarkListView);
