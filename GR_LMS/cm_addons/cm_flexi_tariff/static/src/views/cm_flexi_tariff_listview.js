/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmFlexiTariffDashBoard } from '@cm_flexi_tariff/views/cm_flexi_tariff_dashboard';

export class CmFlexiTariffDashBoardRenderer extends ListRenderer {};

CmFlexiTariffDashBoardRenderer.template = 'cm_flexi_tariff.CmFlexiTariffListView';
CmFlexiTariffDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmFlexiTariffDashBoard})

export const CmFlexiTariffListView = {
    ...listView,
    Renderer: CmFlexiTariffDashBoardRenderer,
};

registry.category("views").add("cm_flexi_tariff_list", CmFlexiTariffListView);
