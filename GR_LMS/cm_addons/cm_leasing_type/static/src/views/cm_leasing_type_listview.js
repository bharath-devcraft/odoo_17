/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmLeasingTypeDashBoard } from '@cm_leasing_type/views/cm_leasing_type_dashboard';

export class CmLeasingTypeDashBoardRenderer extends ListRenderer {};

CmLeasingTypeDashBoardRenderer.template = 'cm_leasing_type.CmLeasingTypeListView';
CmLeasingTypeDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmLeasingTypeDashBoard})

export const CmLeasingTypeListView = {
    ...listView,
    Renderer: CmLeasingTypeDashBoardRenderer,
};

registry.category("views").add("cm_leasing_type_list", CmLeasingTypeListView);
