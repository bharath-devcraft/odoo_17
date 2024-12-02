/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmUserDashBoard } from '@cm_user_mgmt/views/cm_user_dashboard';

export class CmUserDashBoardRenderer extends ListRenderer {};

CmUserDashBoardRenderer.template = 'cm_user_mgmt.CmUserListView';
CmUserDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmUserDashBoard})

export const CmUserListView = {
    ...listView,
    Renderer: CmUserDashBoardRenderer,
};

registry.category("views").add("cm_user_list", CmUserListView);
