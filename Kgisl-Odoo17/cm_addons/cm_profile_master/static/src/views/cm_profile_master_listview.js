/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmProfileMasterDashBoard } from '@cm_profile_master/views/cm_profile_master_dashboard';

export class CmProfileMasterDashBoardRenderer extends ListRenderer {};

CmProfileMasterDashBoardRenderer.template = 'cm_profile_master.CmProfileMasterListView';
CmProfileMasterDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmProfileMasterDashBoard})

export const CmProfileMasterListView = {
    ...listView,
    Renderer: CmProfileMasterDashBoardRenderer,
};

registry.category("views").add("cm_profile_master_list", CmProfileMasterListView);
