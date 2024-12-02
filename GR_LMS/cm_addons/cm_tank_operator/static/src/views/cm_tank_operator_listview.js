/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmTankOperatorDashBoard } from '@cm_tank_operator/views/cm_tank_operator_dashboard';

export class CmTankOperatorDashBoardRenderer extends ListRenderer {};

CmTankOperatorDashBoardRenderer.template = 'cm_tank_operator.CmTankOperatorListView';
CmTankOperatorDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmTankOperatorDashBoard})

export const CmTankOperatorListView = {
    ...listView,
    Renderer: CmTankOperatorDashBoardRenderer,
};

registry.category("views").add("cm_tank_operator_list", CmTankOperatorListView);
