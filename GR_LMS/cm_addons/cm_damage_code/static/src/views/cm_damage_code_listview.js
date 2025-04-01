/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmDamageCodeDashBoard } from '@cm_damage_code/views/cm_damage_code_dashboard';

export class CmDamageCodeDashBoardRenderer extends ListRenderer {};

CmDamageCodeDashBoardRenderer.template = 'cm_damage_code.CmDamageCodeListView';
CmDamageCodeDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmDamageCodeDashBoard})

export const CmDamageCodeListView = {
    ...listView,
    Renderer: CmDamageCodeDashBoardRenderer,
};

registry.category("views").add("cm_damage_code_list", CmDamageCodeListView);
