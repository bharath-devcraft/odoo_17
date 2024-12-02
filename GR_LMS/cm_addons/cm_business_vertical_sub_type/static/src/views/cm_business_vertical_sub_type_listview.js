/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmBusinessVerticalSubTypeDashBoard } from '@cm_business_vertical_sub_type/views/cm_business_vertical_sub_type_dashboard';

export class CmBusinessVerticalSubTypeDashBoardRenderer extends ListRenderer {};

CmBusinessVerticalSubTypeDashBoardRenderer.template = 'cm_business_vertical_sub_type.CmBusinessVerticalSubTypeListView';
CmBusinessVerticalSubTypeDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmBusinessVerticalSubTypeDashBoard})

export const CmBusinessVerticalSubTypeListView = {
    ...listView,
    Renderer: CmBusinessVerticalSubTypeDashBoardRenderer,
};

registry.category("views").add("cm_business_vertical_sub_type_list", CmBusinessVerticalSubTypeListView);
