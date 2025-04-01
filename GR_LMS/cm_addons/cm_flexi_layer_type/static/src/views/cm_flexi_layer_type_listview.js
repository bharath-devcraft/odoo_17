/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmFlexiLayerTypeDashBoard } from '@cm_flexi_layer_type/views/cm_flexi_layer_type_dashboard';

export class CmFlexiLayerTypeDashBoardRenderer extends ListRenderer {};

CmFlexiLayerTypeDashBoardRenderer.template = 'cm_flexi_layer_type.CmFlexiLayerTypeListView';
CmFlexiLayerTypeDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmFlexiLayerTypeDashBoard})

export const CmFlexiLayerTypeListView = {
    ...listView,
    Renderer: CmFlexiLayerTypeDashBoardRenderer,
};

registry.category("views").add("cm_flexi_layer_type_list", CmFlexiLayerTypeListView);
