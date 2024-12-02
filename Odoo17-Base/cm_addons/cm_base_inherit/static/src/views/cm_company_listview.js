/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmCompanyDashBoard } from '@cm_base_inherit/views/cm_company_dashboard';

export class CmCompanyDashBoardRenderer extends ListRenderer {};

CmCompanyDashBoardRenderer.template = 'cm_base_inherit.CmCompanyListView';
CmCompanyDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmCompanyDashBoard})

export const CmCompanyListView = {
    ...listView,
    Renderer: CmCompanyDashBoardRenderer,
};

registry.category("views").add("cm_company_list", CmCompanyListView);
