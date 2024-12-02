/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmDriverMasterDashBoard } from '@cm_driver_master/views/cm_driver_master_dashboard';

export class CmDriverMasterDashBoardRenderer extends ListRenderer {};

CmDriverMasterDashBoardRenderer.template = 'cm_driver_master.CmDriverMasterListView';
CmDriverMasterDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmDriverMasterDashBoard})

export const CmDriverMasterListView = {
    ...listView,
    Renderer: CmDriverMasterDashBoardRenderer,
};

registry.category("views").add("cm_driver_master_list", CmDriverMasterListView);
