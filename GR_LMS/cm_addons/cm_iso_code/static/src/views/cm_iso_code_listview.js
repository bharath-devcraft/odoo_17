/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmIsoCodeDashBoard } from '@cm_iso_code/views/cm_iso_code_dashboard';

export class CmIsoCodeDashBoardRenderer extends ListRenderer {};

CmIsoCodeDashBoardRenderer.template = 'cm_iso_code.CmIsoCodeListView';
CmIsoCodeDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmIsoCodeDashBoard})

export const CmIsoCodeListView = {
    ...listView,
    Renderer: CmIsoCodeDashBoardRenderer,
};

registry.category("views").add("cm_iso_code_list", CmIsoCodeListView);
