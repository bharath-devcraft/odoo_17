/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmCityDashBoard } from '@cm_city/views/cm_city_dashboard';

export class CmCityDashBoardRenderer extends ListRenderer {};

CmCityDashBoardRenderer.template = 'cm_city.CmCityListView';
CmCityDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmCityDashBoard})

export const CmCityListView = {
    ...listView,
    Renderer: CmCityDashBoardRenderer,
};

registry.category("views").add("cm_city_list", CmCityListView);
