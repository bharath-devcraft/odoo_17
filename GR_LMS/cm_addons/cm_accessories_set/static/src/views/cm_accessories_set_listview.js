/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmAccessoriesSetDashBoard } from '@cm_accessories_set/views/cm_accessories_set_dashboard';

export class CmAccessoriesSetDashBoardRenderer extends ListRenderer {};

CmAccessoriesSetDashBoardRenderer.template = 'cm_accessories_set.CmAccessoriesSetListView';
CmAccessoriesSetDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmAccessoriesSetDashBoard})

export const CmAccessoriesSetListView = {
    ...listView,
    Renderer: CmAccessoriesSetDashBoardRenderer,
};

registry.category("views").add("cm_accessories_set_list", CmAccessoriesSetListView);
