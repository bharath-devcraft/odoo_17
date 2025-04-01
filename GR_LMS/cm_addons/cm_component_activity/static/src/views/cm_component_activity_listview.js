/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmComponentActivityDashBoard } from '@cm_component_activity/views/cm_component_activity_dashboard';

export class CmComponentActivityDashBoardRenderer extends ListRenderer {};

CmComponentActivityDashBoardRenderer.template = 'cm_component_activity.CmComponentActivityListView';
CmComponentActivityDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmComponentActivityDashBoard})

export const CmComponentActivityListView = {
    ...listView,
    Renderer: CmComponentActivityDashBoardRenderer,
};

registry.category("views").add("cm_component_activity_list", CmComponentActivityListView);
