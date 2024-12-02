/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmTruckingTariffDashBoard } from '@cm_trucking_tariff/views/cm_trucking_tariff_dashboard';

export class CmTruckingTariffDashBoardRenderer extends ListRenderer {};

CmTruckingTariffDashBoardRenderer.template = 'cm_trucking_tariff.CmTruckingTariffListView';
CmTruckingTariffDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmTruckingTariffDashBoard})

export const CmTruckingTariffListView = {
    ...listView,
    Renderer: CmTruckingTariffDashBoardRenderer,
};

registry.category("views").add("cm_trucking_tariff_list", CmTruckingTariffListView);
