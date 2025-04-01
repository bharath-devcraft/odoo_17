/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmOpDoorTariffDashBoard } from '@cm_door_tariff/views/cm_op_door_tariff_dashboard';

export class CmOpDoorTariffDashBoardRenderer extends ListRenderer {};

CmOpDoorTariffDashBoardRenderer.template = 'cm_door_tariff.CmOpDoorTariffListView';
CmOpDoorTariffDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmOpDoorTariffDashBoard})

export const CmOpDoorTariffListView = {
    ...listView,
    Renderer: CmOpDoorTariffDashBoardRenderer,
};

registry.category("views").add("cm_op_door_tariff_list", CmOpDoorTariffListView);
