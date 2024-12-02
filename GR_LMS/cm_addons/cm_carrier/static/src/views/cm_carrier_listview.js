/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmCarrierDashBoard } from '@cm_carrier/views/cm_carrier_dashboard';

export class CmCarrierDashBoardRenderer extends ListRenderer {};

CmCarrierDashBoardRenderer.template = 'cm_carrier.CmCarrierListView';
CmCarrierDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmCarrierDashBoard})

export const CmCarrierListView = {
    ...listView,
    Renderer: CmCarrierDashBoardRenderer,
};

registry.category("views").add("cm_carrier_list", CmCarrierListView);
