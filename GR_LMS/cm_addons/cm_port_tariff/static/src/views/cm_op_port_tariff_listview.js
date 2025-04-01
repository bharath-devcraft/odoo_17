/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmOpPortTariffDashBoard } from '@cm_port_tariff/views/cm_op_port_tariff_dashboard';

export class CmOpPortTariffDashBoardRenderer extends ListRenderer {};

CmOpPortTariffDashBoardRenderer.template = 'cm_port_tariff.CmOpPortTariffListView';
CmOpPortTariffDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmOpPortTariffDashBoard})

export const CmOpPortTariffListView = {
    ...listView,
    Renderer: CmOpPortTariffDashBoardRenderer,
};

registry.category("views").add("cm_op_port_tariff_list", CmOpPortTariffListView);
