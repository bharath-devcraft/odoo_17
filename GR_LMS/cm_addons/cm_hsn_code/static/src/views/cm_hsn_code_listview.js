/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmHsnCodeDashBoard } from '@cm_hsn_code/views/cm_hsn_code_dashboard';

export class CmHsnCodeDashBoardRenderer extends ListRenderer {};

CmHsnCodeDashBoardRenderer.template = 'cm_hsn_code.CmHsnCodeListView';
CmHsnCodeDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmHsnCodeDashBoard})

export const CmHsnCodeListView = {
    ...listView,
    Renderer: CmHsnCodeDashBoardRenderer,
};

registry.category("views").add("cm_hsn_code_list", CmHsnCodeListView);
