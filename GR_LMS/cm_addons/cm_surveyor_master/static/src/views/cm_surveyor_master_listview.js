/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmSurveyorMasterDashBoard } from '@cm_surveyor_master/views/cm_surveyor_master_dashboard';

export class CmSurveyorMasterDashBoardRenderer extends ListRenderer {};

CmSurveyorMasterDashBoardRenderer.template = 'cm_surveyor_master.CmSurveyorMasterListView';
CmSurveyorMasterDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmSurveyorMasterDashBoard})

export const CmSurveyorMasterListView = {
    ...listView,
    Renderer: CmSurveyorMasterDashBoardRenderer,
};

registry.category("views").add("cm_surveyor_master_list", CmSurveyorMasterListView);
