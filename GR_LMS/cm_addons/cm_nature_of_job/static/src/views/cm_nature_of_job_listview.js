/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmNatureOfJobDashBoard } from '@cm_nature_of_job/views/cm_nature_of_job_dashboard';

export class CmNatureOfJobDashBoardRenderer extends ListRenderer {};

CmNatureOfJobDashBoardRenderer.template = 'cm_nature_of_job.CmNatureOfJobListView';
CmNatureOfJobDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmNatureOfJobDashBoard})

export const CmNatureOfJobListView = {
    ...listView,
    Renderer: CmNatureOfJobDashBoardRenderer,
};

registry.category("views").add("cm_nature_of_job_list", CmNatureOfJobListView);
