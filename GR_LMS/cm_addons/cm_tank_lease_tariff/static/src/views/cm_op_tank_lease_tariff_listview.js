/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmOpTankLeaseTariffDashBoard } from '@cm_tank_lease_tariff/views/cm_op_tank_lease_tariff_dashboard';

export class CmOpTankLeaseTariffDashBoardRenderer extends ListRenderer {};

CmOpTankLeaseTariffDashBoardRenderer.template = 'cm_tank_lease_tariff.CmOpTankLeaseTariffListView';
CmOpTankLeaseTariffDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmOpTankLeaseTariffDashBoard})

export const CmOpTankLeaseTariffListView = {
    ...listView,
    Renderer: CmOpTankLeaseTariffDashBoardRenderer,
};

registry.category("views").add("cm_op_tank_lease_tariff_list", CmOpTankLeaseTariffListView);
