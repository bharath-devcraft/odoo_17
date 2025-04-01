/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmAgentRestrictionDashBoard } from '@cm_agent_restriction/views/cm_agent_restriction_dashboard';

export class CmAgentRestrictionDashBoardRenderer extends ListRenderer {};

CmAgentRestrictionDashBoardRenderer.template = 'cm_agent_restriction.CmAgentRestrictionListView';
CmAgentRestrictionDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmAgentRestrictionDashBoard})

export const CmAgentRestrictionListView = {
    ...listView,
    Renderer: CmAgentRestrictionDashBoardRenderer,
};

registry.category("views").add("cm_agent_restriction_list", CmAgentRestrictionListView);
