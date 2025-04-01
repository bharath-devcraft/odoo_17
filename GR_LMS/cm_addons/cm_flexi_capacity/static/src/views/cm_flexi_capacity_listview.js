/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmFlexiCapacityDashBoard } from '@cm_flexi_capacity/views/cm_flexi_capacity_dashboard';

export class CmFlexiCapacityDashBoardRenderer extends ListRenderer {};

CmFlexiCapacityDashBoardRenderer.template = 'cm_flexi_capacity.CmFlexiCapacityListView';
CmFlexiCapacityDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmFlexiCapacityDashBoard})

export const CmFlexiCapacityListView = {
    ...listView,
    Renderer: CmFlexiCapacityDashBoardRenderer,
};

registry.category("views").add("cm_flexi_capacity_list", CmFlexiCapacityListView);
