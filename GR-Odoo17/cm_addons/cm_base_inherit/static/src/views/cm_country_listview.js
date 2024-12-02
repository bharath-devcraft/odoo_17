/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmCountryDashBoard } from '@cm_base_inherit/views/cm_country_dashboard';

export class CmCountryDashBoardRenderer extends ListRenderer {};

CmCountryDashBoardRenderer.template = 'cm_base_inherit.CmCountryListView';
CmCountryDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmCountryDashBoard})

export const CmCountryListView = {
    ...listView,
    Renderer: CmCountryDashBoardRenderer,
};

registry.category("views").add("cm_country_list", CmCountryListView);
