/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmRailTariffDashBoard } from '@cm_rail_tariff/views/cm_rail_tariff_dashboard';

export class CmRailTariffDashBoardRenderer extends ListRenderer {};

CmRailTariffDashBoardRenderer.template = 'cm_rail_tariff.CmRailTariffListView';
CmRailTariffDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmRailTariffDashBoard})

export const CmRailTariffListView = {
    ...listView,
    Renderer: CmRailTariffDashBoardRenderer,
};

registry.category("views").add("cm_rail_tariff_list", CmRailTariffListView);
