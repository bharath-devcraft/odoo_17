/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmExchangeRateDashBoard } from '@cm_exchange_rate/views/cm_exchange_rate_dashboard';

export class CmExchangeRateDashBoardRenderer extends ListRenderer {};

CmExchangeRateDashBoardRenderer.template = 'cm_exchange_rate.CmExchangeRateListView';
CmExchangeRateDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmExchangeRateDashBoard})

export const CmExchangeRateListView = {
    ...listView,
    Renderer: CmExchangeRateDashBoardRenderer,
};

registry.category("views").add("cm_exchange_rate_list", CmExchangeRateListView);
