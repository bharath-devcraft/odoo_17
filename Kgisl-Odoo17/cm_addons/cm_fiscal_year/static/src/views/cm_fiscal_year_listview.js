/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmFiscalYearDashBoard } from '@cm_fiscal_year/views/cm_fiscal_year_dashboard';

export class CmFiscalYearDashBoardRenderer extends ListRenderer {};

CmFiscalYearDashBoardRenderer.template = 'cm_fiscal_year.CmFiscalYearListView';
CmFiscalYearDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CmFiscalYearDashBoard})

export const CmFiscalYearListView = {
    ...listView,
    Renderer: CmFiscalYearDashBoardRenderer,
};

registry.category("views").add("cm_fiscal_year_list", CmFiscalYearListView);
