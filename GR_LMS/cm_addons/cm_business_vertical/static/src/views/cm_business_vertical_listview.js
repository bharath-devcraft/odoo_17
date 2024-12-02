/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmBusinessVerticalDashBoard } from '@cm_business_vertical/views/cm_business_vertical_dashboard';

export class CmBusinessVerticalDashBoardRenderer extends ListRenderer {};

CmBusinessVerticalDashBoardRenderer.template = 'cm_business_vertical.CmBusinessVerticalListView';
CmBusinessVerticalDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmBusinessVerticalDashBoard})

export const CmBusinessVerticalListView = {
    ...listView,
    Renderer: CmBusinessVerticalDashBoardRenderer,
};

registry.category("views").add("cm_business_vertical_list", CmBusinessVerticalListView);
