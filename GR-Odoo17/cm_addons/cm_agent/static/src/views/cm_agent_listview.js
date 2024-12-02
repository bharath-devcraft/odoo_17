/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmAgentDashBoard } from '@cm_agent/views/cm_agent_dashboard';

export class CmAgentDashBoardRenderer extends ListRenderer {};

CmAgentDashBoardRenderer.template = 'cm_agent.CmAgentListView';
CmAgentDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmAgentDashBoard})

export const CmAgentListView = {
    ...listView,
    Renderer: CmAgentDashBoardRenderer,
};

registry.category("views").add("cm_agent_list", CmAgentListView);
