/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmShipmentTermDashBoard } from '@cm_shipment_term/views/cm_shipment_term_dashboard';

export class CmShipmentTermDashBoardRenderer extends ListRenderer {};

CmShipmentTermDashBoardRenderer.template = 'cm_shipment_term.CmShipmentTermListView';
CmShipmentTermDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmShipmentTermDashBoard})

export const CmShipmentTermListView = {
    ...listView,
    Renderer: CmShipmentTermDashBoardRenderer,
};

registry.category("views").add("cm_shipment_term_list", CmShipmentTermListView);
