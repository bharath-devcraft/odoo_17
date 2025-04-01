/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CtPiPoEntryDashBoard } from '@ct_pipo_entry/views/ct_pipo_entry_dashboard';

export class CtPiPoEntryDashBoardRenderer extends ListRenderer {};

CtPiPoEntryDashBoardRenderer.template = 'ct_pipo_entry.CtPiPoEntryListView';
CtPiPoEntryDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CtPiPoEntryDashBoard})

export const CtPiPoEntryListView = {
    ...listView,
    Renderer: CtPiPoEntryDashBoardRenderer,
};

registry.category("views").add("ct_pipo_entry_list", CtPiPoEntryListView);
