/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmOpDepotTariffDashBoard } from '@cm_depot_tariff/views/cm_op_depot_tariff_dashboard';

export class CmOpDepotTariffDashBoardRenderer extends ListRenderer {};

CmOpDepotTariffDashBoardRenderer.template = 'cm_depot_tariff.CmOpDepotTariffListView';
CmOpDepotTariffDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmOpDepotTariffDashBoard})

export const CmOpDepotTariffListView = {
    ...listView,
    Renderer: CmOpDepotTariffDashBoardRenderer,
};

registry.category("views").add("cm_op_depot_tariff_list", CmOpDepotTariffListView);
