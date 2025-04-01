/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmOperatorTariffDashBoard } from '@cm_operator_tariff/views/cm_operator_tariff_dashboard';

export class CmOperatorTariffDashBoardRenderer extends ListRenderer {};

CmOperatorTariffDashBoardRenderer.template = 'cm_operator_tariff.CmOperatorTariffListView';
CmOperatorTariffDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmOperatorTariffDashBoard})

export const CmOperatorTariffListView = {
    ...listView,
    Renderer: CmOperatorTariffDashBoardRenderer,
};

registry.category("views").add("cm_operator_tariff_list", CmOperatorTariffListView);
