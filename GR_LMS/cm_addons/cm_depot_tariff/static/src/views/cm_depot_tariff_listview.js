/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmDepotTariffDashBoard } from '@cm_depot_tariff/views/cm_depot_tariff_dashboard';

export class CmDepotTariffDashBoardRenderer extends ListRenderer {};

CmDepotTariffDashBoardRenderer.template = 'cm_depot_tariff.CmDepotTariffListView';
CmDepotTariffDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmDepotTariffDashBoard})

export const CmDepotTariffListView = {
    ...listView,
    Renderer: CmDepotTariffDashBoardRenderer,
};

registry.category("views").add("cm_depot_tariff_list", CmDepotTariffListView);
