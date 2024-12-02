/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmServiceDashBoard } from '@cm_service/views/cm_service_dashboard';

export class CmServiceDashBoardRenderer extends ListRenderer {};

CmServiceDashBoardRenderer.template = 'cm_service.CmServiceListView';
CmServiceDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmServiceDashBoard})

export const CmServiceListView = {
    ...listView,
    Renderer: CmServiceDashBoardRenderer,
};

registry.category("views").add("cm_service_list", CmServiceListView);
