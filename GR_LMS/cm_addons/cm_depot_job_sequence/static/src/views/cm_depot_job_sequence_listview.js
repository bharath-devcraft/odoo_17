/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmDepotJobSequenceDashBoard } from '@cm_depot_job_sequence/views/cm_depot_job_sequence_dashboard';

export class CmDepotJobSequenceDashBoardRenderer extends ListRenderer {};

CmDepotJobSequenceDashBoardRenderer.template = 'cm_depot_job_sequence.CmDepotJobSequenceListView';
CmDepotJobSequenceDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmDepotJobSequenceDashBoard})

export const CmDepotJobSequenceListView = {
    ...listView,
    Renderer: CmDepotJobSequenceDashBoardRenderer,
};

registry.category("views").add("cm_depot_job_sequence_list", CmDepotJobSequenceListView);
