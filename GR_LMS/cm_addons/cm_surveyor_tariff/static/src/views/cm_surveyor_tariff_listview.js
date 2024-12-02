/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmSurveyorTariffDashBoard } from '@cm_surveyor_tariff/views/cm_surveyor_tariff_dashboard';

export class CmSurveyorTariffDashBoardRenderer extends ListRenderer {};

CmSurveyorTariffDashBoardRenderer.template = 'cm_surveyor_tariff.CmSurveyorTariffListView';
CmSurveyorTariffDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmSurveyorTariffDashBoard})

export const CmSurveyorTariffListView = {
    ...listView,
    Renderer: CmSurveyorTariffDashBoardRenderer,
};

registry.category("views").add("cm_surveyor_tariff_list", CmSurveyorTariffListView);
