/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmPortTariffDashBoard } from '@cm_port_tariff/views/cm_port_tariff_dashboard';

export class CmPortTariffDashBoardRenderer extends ListRenderer {};

CmPortTariffDashBoardRenderer.template = 'cm_port_tariff.CmPortTariffListView';
CmPortTariffDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmPortTariffDashBoard})

export const CmPortTariffListView = {
    ...listView,
    Renderer: CmPortTariffDashBoardRenderer,
};

registry.category("views").add("cm_port_tariff_list", CmPortTariffListView);
