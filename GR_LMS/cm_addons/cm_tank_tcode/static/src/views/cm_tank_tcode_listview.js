/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmTankTcodeDashBoard } from '@cm_tank_tcode/views/cm_tank_tcode_dashboard';

export class CmTankTcodeDashBoardRenderer extends ListRenderer {};

CmTankTcodeDashBoardRenderer.template = 'cm_tank_tcode.CmTankTcodeListView';
CmTankTcodeDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmTankTcodeDashBoard})

export const CmTankTcodeListView = {
    ...listView,
    Renderer: CmTankTcodeDashBoardRenderer,
};

registry.category("views").add("cm_tank_tcode_list", CmTankTcodeListView);
