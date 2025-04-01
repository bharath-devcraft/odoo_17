/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmTermsConditionsDashBoard } from '@cm_terms_conditions/views/cm_terms_conditions_dashboard';

export class CmTermsConditionsDashBoardRenderer extends ListRenderer {};

CmTermsConditionsDashBoardRenderer.template = 'cm_terms_conditions.CmTermsConditionsListView';
CmTermsConditionsDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmTermsConditionsDashBoard})

export const CmTermsConditionsListView = {
    ...listView,
    Renderer: CmTermsConditionsDashBoardRenderer,
};

registry.category("views").add("cm_terms_conditions_list", CmTermsConditionsListView);
