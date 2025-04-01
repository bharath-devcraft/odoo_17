/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmAgentCommissionDashBoard } from '@cm_agent_commission/views/cm_agent_commission_dashboard';

export class CmAgentCommissionDashBoardRenderer extends ListRenderer {};

CmAgentCommissionDashBoardRenderer.template = 'cm_agent_commission.CmAgentCommissionListView';
CmAgentCommissionDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmAgentCommissionDashBoard})

export const CmAgentCommissionListView = {
    ...listView,
    Renderer: CmAgentCommissionDashBoardRenderer,
};

registry.category("views").add("cm_agent_commission_list", CmAgentCommissionListView);
