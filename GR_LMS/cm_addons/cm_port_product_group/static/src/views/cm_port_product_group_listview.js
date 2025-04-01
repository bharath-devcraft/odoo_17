/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmPortProductGroupDashBoard } from '@cm_port_product_group/views/cm_port_product_group_dashboard';

export class CmPortProductGroupDashBoardRenderer extends ListRenderer {};

CmPortProductGroupDashBoardRenderer.template = 'cm_port_product_group.CmPortProductGroupListView';
CmPortProductGroupDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmPortProductGroupDashBoard})

export const CmPortProductGroupListView = {
    ...listView,
    Renderer: CmPortProductGroupDashBoardRenderer,
};

registry.category("views").add("cm_port_product_group_list", CmPortProductGroupListView);
