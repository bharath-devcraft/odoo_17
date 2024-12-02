/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmCountryStateDashBoard } from '@cm_base_inherit/views/cm_country_state_dashboard';

export class CmCountryStateDashBoardRenderer extends ListRenderer {};

CmCountryStateDashBoardRenderer.template = 'cm_base_inherit.CmCountryStateListView';
CmCountryStateDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmCountryStateDashBoard})

export const CmCountryStateListView = {
    ...listView,
    Renderer: CmCountryStateDashBoardRenderer,
};

registry.category("views").add("cm_country_state_list", CmCountryStateListView);
