/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmChargesHeadsDashBoard } from '@cm_charges_heads/views/cm_charges_heads_dashboard';

export class CmChargesHeadsDashBoardRenderer extends ListRenderer {};

CmChargesHeadsDashBoardRenderer.template = 'cm_charges_heads.CmChargesHeadsListView';
CmChargesHeadsDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmChargesHeadsDashBoard})

export const CmChargesHeadsListView = {
    ...listView,
    Renderer: CmChargesHeadsDashBoardRenderer,
};

registry.category("views").add("cm_charges_heads_list", CmChargesHeadsListView);
