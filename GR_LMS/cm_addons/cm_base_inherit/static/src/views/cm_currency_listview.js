/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmCurrencyDashBoard } from '@cm_base_inherit/views/cm_currency_dashboard';

export class CmCurrencyDashBoardRenderer extends ListRenderer {};

CmCurrencyDashBoardRenderer.template = 'cm_base_inherit.CmCurrencyListView';
CmCurrencyDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmCurrencyDashBoard})

export const CmCurrencyListView = {
    ...listView,
    Renderer: CmCurrencyDashBoardRenderer,
};

registry.category("views").add("cm_currency_list", CmCurrencyListView);
