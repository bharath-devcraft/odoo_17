/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmMasterDashBoard } from '@cm_master/views/cm_master_dashboard';

export class CmMasterDashBoardRenderer extends ListRenderer {};

CmMasterDashBoardRenderer.template = 'cm_master.CmMasterListView';
CmMasterDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmMasterDashBoard})

export const CmMasterListView = {
    ...listView,
    Renderer: CmMasterDashBoardRenderer,
};

registry.category("views").add("cm_master_list", CmMasterListView);
