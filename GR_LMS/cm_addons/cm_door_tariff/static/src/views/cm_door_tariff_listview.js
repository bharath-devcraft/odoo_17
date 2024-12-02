/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmDoorTariffDashBoard } from '@cm_door_tariff/views/cm_door_tariff_dashboard';

export class CmDoorTariffDashBoardRenderer extends ListRenderer {};

CmDoorTariffDashBoardRenderer.template = 'cm_door_tariff.CmDoorTariffListView';
CmDoorTariffDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmDoorTariffDashBoard})

export const CmDoorTariffListView = {
    ...listView,
    Renderer: CmDoorTariffDashBoardRenderer,
};

registry.category("views").add("cm_door_tariff_list", CmDoorTariffListView);
