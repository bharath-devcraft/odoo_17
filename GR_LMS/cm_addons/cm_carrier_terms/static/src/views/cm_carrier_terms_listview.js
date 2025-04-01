/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmCarrierTermsDashBoard } from '@cm_carrier_terms/views/cm_carrier_terms_dashboard';

export class CmCarrierTermsDashBoardRenderer extends ListRenderer {};

CmCarrierTermsDashBoardRenderer.template = 'cm_carrier_terms.CmCarrierTermsListView';
CmCarrierTermsDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmCarrierTermsDashBoard})

export const CmCarrierTermsListView = {
    ...listView,
    Renderer: CmCarrierTermsDashBoardRenderer,
};

registry.category("views").add("cm_carrier_terms_list", CmCarrierTermsListView);
