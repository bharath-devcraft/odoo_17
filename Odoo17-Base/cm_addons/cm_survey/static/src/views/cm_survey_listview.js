/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmSurveyDashBoard } from '@cm_survey/views/cm_survey_dashboard';

export class CmSurveyDashBoardRenderer extends ListRenderer {};

CmSurveyDashBoardRenderer.template = 'cm_survey.CmSurveyListView';
CmSurveyDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmSurveyDashBoard})

export const CmSurveyListView = {
    ...listView,
    Renderer: CmSurveyDashBoardRenderer,
};

registry.category("views").add("cm_survey_list", CmSurveyListView);
