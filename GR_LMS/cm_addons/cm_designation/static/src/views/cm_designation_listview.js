/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmDesignationDashBoard } from '@cm_designation/views/cm_designation_dashboard';

export class CmDesignationDashBoardRenderer extends ListRenderer {};

CmDesignationDashBoardRenderer.template = 'cm_designation.CmDesignationListView';
CmDesignationDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmDesignationDashBoard})

export const CmDesignationListView = {
    ...listView,
    Renderer: CmDesignationDashBoardRenderer,
};

registry.category("views").add("cm_designation_list", CmDesignationListView);
