/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CtStoreIssueDashBoard } from '@ct_store_issue/views/ct_store_issue_dashboard';

export class CtStoreIssueDashBoardRenderer extends ListRenderer {};

CtStoreIssueDashBoardRenderer.template = 'ct_store_issue.CtStoreIssueListView';
CtStoreIssueDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CtStoreIssueDashBoard})

export const CtStoreIssueListView = {
    ...listView,
    Renderer: CtStoreIssueDashBoardRenderer,
};

registry.category("views").add("ct_store_issue_list", CtStoreIssueListView);
