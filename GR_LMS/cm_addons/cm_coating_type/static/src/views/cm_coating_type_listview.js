/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmCoatingTypeDashBoard } from '@cm_coating_type/views/cm_coating_type_dashboard';

export class CmCoatingTypeDashBoardRenderer extends ListRenderer {};

CmCoatingTypeDashBoardRenderer.template = 'cm_coating_type.CmCoatingTypeListView';
CmCoatingTypeDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmCoatingTypeDashBoard})

export const CmCoatingTypeListView = {
    ...listView,
    Renderer: CmCoatingTypeDashBoardRenderer,
};

registry.category("views").add("cm_coating_type_list", CmCoatingTypeListView);
