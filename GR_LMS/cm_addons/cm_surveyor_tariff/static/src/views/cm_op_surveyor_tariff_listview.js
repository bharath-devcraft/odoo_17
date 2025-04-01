/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmOpSurveyorTariffDashBoard } from '@cm_surveyor_tariff/views/cm_op_surveyor_tariff_dashboard';

export class CmOpSurveyorTariffDashBoardRenderer extends ListRenderer {};

CmOpSurveyorTariffDashBoardRenderer.template = 'cm_surveyor_tariff.CmOpSurveyorTariffListView';
CmOpSurveyorTariffDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmOpSurveyorTariffDashBoard})

export const CmOpSurveyorTariffListView = {
    ...listView,
    Renderer: CmOpSurveyorTariffDashBoardRenderer,
};

registry.category("views").add("cm_op_surveyor_tariff_list", CmOpSurveyorTariffListView);
