/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmMocDashBoard } from '@cm_moc/views/cm_moc_dashboard';

export class CmMocDashBoardRenderer extends ListRenderer {};

CmMocDashBoardRenderer.template = 'cm_moc.CmMocListView';
CmMocDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmMocDashBoard})

export const CmMocListView = {
    ...listView,
    Renderer: CmMocDashBoardRenderer,
};

registry.category("views").add("cm_moc_list", CmMocListView);
