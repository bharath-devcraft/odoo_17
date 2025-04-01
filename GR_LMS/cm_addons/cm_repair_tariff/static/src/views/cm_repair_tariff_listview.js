/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmRepairTariffDashBoard } from '@cm_repair_tariff/views/cm_repair_tariff_dashboard';

export class CmRepairTariffDashBoardRenderer extends ListRenderer {};

CmRepairTariffDashBoardRenderer.template = 'cm_repair_tariff.CmRepairTariffListView';
CmRepairTariffDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmRepairTariffDashBoard})

export const CmRepairTariffListView = {
    ...listView,
    Renderer: CmRepairTariffDashBoardRenderer,
};

registry.category("views").add("cm_repair_tariff_list", CmRepairTariffListView);
