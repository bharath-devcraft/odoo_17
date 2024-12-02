/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmPortTerminalDashBoard } from '@cm_port_terminal/views/cm_port_terminal_dashboard';

export class CmPortTerminalDashBoardRenderer extends ListRenderer {};

CmPortTerminalDashBoardRenderer.template = 'cm_port_terminal.CmPortTerminalListView';
CmPortTerminalDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmPortTerminalDashBoard})

export const CmPortTerminalListView = {
    ...listView,
    Renderer: CmPortTerminalDashBoardRenderer,
};

registry.category("views").add("cm_port_terminal_list", CmPortTerminalListView);
