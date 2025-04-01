/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmItemDashBoard } from '@cm_item/views/cm_item_dashboard';

export class CmItemDashBoardRenderer extends ListRenderer {};

CmItemDashBoardRenderer.template = 'cm_item.CmItemListView';
CmItemDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmItemDashBoard})

export const CmItemListView = {
    ...listView,
    Renderer: CmItemDashBoardRenderer,
};

registry.category("views").add("cm_item_list", CmItemListView);
