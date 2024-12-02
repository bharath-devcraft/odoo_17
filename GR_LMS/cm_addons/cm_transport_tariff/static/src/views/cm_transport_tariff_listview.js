/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmTransportTariffDashBoard } from '@cm_transport_tariff/views/cm_transport_tariff_dashboard';

export class CmTransportTariffDashBoardRenderer extends ListRenderer {};

CmTransportTariffDashBoardRenderer.template = 'cm_transport_tariff.CmTransportTariffListView';
CmTransportTariffDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmTransportTariffDashBoard})

export const CmTransportTariffListView = {
    ...listView,
    Renderer: CmTransportTariffDashBoardRenderer,
};

registry.category("views").add("cm_transport_tariff_list", CmTransportTariffListView);
