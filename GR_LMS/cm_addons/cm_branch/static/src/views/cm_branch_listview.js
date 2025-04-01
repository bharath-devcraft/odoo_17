/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmBranchDashBoard } from '@cm_branch/views/cm_branch_dashboard';

export class CmBranchDashBoardRenderer extends ListRenderer {};

CmBranchDashBoardRenderer.template = 'cm_branch.CmBranchListView';
CmBranchDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmBranchDashBoard})

export const CmBranchListView = {
    ...listView,
    Renderer: CmBranchDashBoardRenderer,
};

registry.category("views").add("cm_branch_list", CmBranchListView);
