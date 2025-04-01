/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmShipperInstructionDashBoard } from '@cm_shipper_instruction/views/cm_shipper_instruction_dashboard';

export class CmShipperInstructionDashBoardRenderer extends ListRenderer {};

CmShipperInstructionDashBoardRenderer.template = 'cm_shipper_instruction.CmShipperInstructionListView';
CmShipperInstructionDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmShipperInstructionDashBoard})

export const CmShipperInstructionListView = {
    ...listView,
    Renderer: CmShipperInstructionDashBoardRenderer,
};

registry.category("views").add("cm_shipper_instruction_list", CmShipperInstructionListView);
