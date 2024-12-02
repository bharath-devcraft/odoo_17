/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmTankOperatorsDashBoard } from '@cm_tank_operators/views/cm_tank_operators_dashboard';

export class CmTankOperatorsDashBoardRenderer extends ListRenderer {};

CmTankOperatorsDashBoardRenderer.template = 'cm_tank_operators.CmTankOperatorsListView';
CmTankOperatorsDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmTankOperatorsDashBoard})

export const CmTankOperatorsListView = {
    ...listView,
    Renderer: CmTankOperatorsDashBoardRenderer,
};

registry.category("views").add("cm_tank_operators_list", CmTankOperatorsListView);
