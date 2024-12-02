/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmTankLeaseTariffDashBoard } from '@cm_tank_lease_tariff/views/cm_tank_lease_tariff_dashboard';

export class CmTankLeaseTariffDashBoardRenderer extends ListRenderer {};

CmTankLeaseTariffDashBoardRenderer.template = 'cm_tank_lease_tariff.CmTankLeaseTariffListView';
CmTankLeaseTariffDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmTankLeaseTariffDashBoard})

export const CmTankLeaseTariffListView = {
    ...listView,
    Renderer: CmTankLeaseTariffDashBoardRenderer,
};

registry.category("views").add("cm_tank_lease_tariff_list", CmTankLeaseTariffListView);
