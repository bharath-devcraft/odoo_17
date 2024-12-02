/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmTerminalDashBoard } from '@cm_terminal/views/cm_terminal_dashboard';

export class CmTerminalDashBoardRenderer extends ListRenderer {};

CmTerminalDashBoardRenderer.template = 'cm_terminal.CmTerminalListView';
CmTerminalDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmTerminalDashBoard})

export const CmTerminalListView = {
    ...listView,
    Renderer: CmTerminalDashBoardRenderer,
};

registry.category("views").add("cm_terminal_list", CmTerminalListView);
