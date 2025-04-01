/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmOpRailTariffDashBoard } from '@cm_rail_tariff/views/cm_op_rail_tariff_dashboard';

export class CmOpRailTariffDashBoardRenderer extends ListRenderer {};

CmOpRailTariffDashBoardRenderer.template = 'cm_rail_tariff.CmOpRailTariffListView';
CmOpRailTariffDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmOpRailTariffDashBoard})

export const CmOpRailTariffListView = {
    ...listView,
    Renderer: CmOpRailTariffDashBoardRenderer,
};

registry.category("views").add("cm_op_rail_tariff_list", CmOpRailTariffListView);
