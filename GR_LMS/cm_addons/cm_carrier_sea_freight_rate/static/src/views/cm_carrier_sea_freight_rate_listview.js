/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmCarrierSeaFreightRateDashBoard } from '@cm_carrier_sea_freight_rate/views/cm_carrier_sea_freight_rate_dashboard';

export class CmCarrierSeaFreightRateDashBoardRenderer extends ListRenderer {};

CmCarrierSeaFreightRateDashBoardRenderer.template = 'cm_carrier_sea_freight_rate.CmCarrierSeaFreightRateListView';
CmCarrierSeaFreightRateDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmCarrierSeaFreightRateDashBoard})

export const CmCarrierSeaFreightRateListView = {
    ...listView,
    Renderer: CmCarrierSeaFreightRateDashBoardRenderer,
};

registry.category("views").add("cm_carrier_sea_freight_rate_list", CmCarrierSeaFreightRateListView);
