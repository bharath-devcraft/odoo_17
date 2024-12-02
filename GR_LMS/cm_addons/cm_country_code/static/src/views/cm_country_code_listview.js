/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmCountryCodeDashBoard } from '@cm_country_code/views/cm_country_code_dashboard';

export class CmCountryCodeDashBoardRenderer extends ListRenderer {};

CmCountryCodeDashBoardRenderer.template = 'cm_country_code.CmCountryCodeListView';
CmCountryCodeDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmCountryCodeDashBoard})

export const CmCountryCodeListView = {
    ...listView,
    Renderer: CmCountryCodeDashBoardRenderer,
};

registry.category("views").add("cm_country_code_list", CmCountryCodeListView);
