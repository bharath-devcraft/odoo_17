/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmCustomsWorkTariffDashBoard } from '@cm_customs_work_tariff/views/cm_customs_work_tariff_dashboard';

export class CmCustomsWorkTariffDashBoardRenderer extends ListRenderer {};

CmCustomsWorkTariffDashBoardRenderer.template = 'cm_customs_work_tariff.CmCustomsWorkTariffListView';
CmCustomsWorkTariffDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmCustomsWorkTariffDashBoard})

export const CmCustomsWorkTariffListView = {
    ...listView,
    Renderer: CmCustomsWorkTariffDashBoardRenderer,
};

registry.category("views").add("cm_customs_work_tariff_list", CmCustomsWorkTariffListView);
