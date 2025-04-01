/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmTaxMappingDashBoard } from '@cm_tax_mapping/views/cm_tax_mapping_dashboard';

export class CmTaxMappingDashBoardRenderer extends ListRenderer {};

CmTaxMappingDashBoardRenderer.template = 'cm_tax_mapping.CmTaxMappingListView';
CmTaxMappingDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmTaxMappingDashBoard})

export const CmTaxMappingListView = {
    ...listView,
    Renderer: CmTaxMappingDashBoardRenderer,
};

registry.category("views").add("cm_tax_mapping_list", CmTaxMappingListView);
