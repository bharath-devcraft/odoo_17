/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmPortDashBoard } from '@cm_port/views/cm_port_dashboard';

export class CmPortDashBoardRenderer extends ListRenderer {};

CmPortDashBoardRenderer.template = 'cm_port.CmPortListView';
CmPortDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmPortDashBoard})

export const CmPortListView = {
    ...listView,
    Renderer: CmPortDashBoardRenderer,
};

registry.category("views").add("cm_port_list", CmPortListView);
