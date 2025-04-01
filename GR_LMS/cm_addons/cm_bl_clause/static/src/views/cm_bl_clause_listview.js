/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmBlClauseDashBoard } from '@cm_bl_clause/views/cm_bl_clause_dashboard';

export class CmBlClauseDashBoardRenderer extends ListRenderer {};

CmBlClauseDashBoardRenderer.template = 'cm_bl_clause.CmBlClauseListView';
CmBlClauseDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmBlClauseDashBoard})

export const CmBlClauseListView = {
    ...listView,
    Renderer: CmBlClauseDashBoardRenderer,
};

registry.category("views").add("cm_bl_clause_list", CmBlClauseListView);
