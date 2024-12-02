/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmProductTemplateGeneralDashBoard } from '@cm_product_inherit/views/cm_product_template_general_dashboard';

export class CmProductTemplateGeneralDashBoardRenderer extends ListRenderer {};

CmProductTemplateGeneralDashBoardRenderer.template = 'cm_product_inherit.CmProductTemplateGeneralListView';
CmProductTemplateGeneralDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmProductTemplateGeneralDashBoard})

export const CmProductTemplateGeneralListView = {
    ...listView,
    Renderer: CmProductTemplateGeneralDashBoardRenderer,
};

registry.category("views").add("cm_product_template_general_list", CmProductTemplateGeneralListView);
