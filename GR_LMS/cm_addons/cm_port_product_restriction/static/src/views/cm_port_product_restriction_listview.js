/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmPortProductRestrictionDashBoard } from '@cm_port_product_restriction/views/cm_port_product_restriction_dashboard';

export class CmPortProductRestrictionDashBoardRenderer extends ListRenderer {};

CmPortProductRestrictionDashBoardRenderer.template = 'cm_port_product_restriction.CmPortProductRestrictionListView';
CmPortProductRestrictionDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmPortProductRestrictionDashBoard})

export const CmPortProductRestrictionListView = {
    ...listView,
    Renderer: CmPortProductRestrictionDashBoardRenderer,
};

registry.category("views").add("cm_port_product_restriction_list", CmPortProductRestrictionListView);
