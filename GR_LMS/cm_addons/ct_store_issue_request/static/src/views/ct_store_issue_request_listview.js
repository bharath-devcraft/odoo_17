/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CtStoreIssueRequestDashBoard } from '@ct_store_issue_request/views/ct_store_issue_request_dashboard';

export class CtStoreIssueRequestDashBoardRenderer extends ListRenderer {};

CtStoreIssueRequestDashBoardRenderer.template = 'ct_store_issue_request.CtStoreIssueRequestListView';
CtStoreIssueRequestDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CtStoreIssueRequestDashBoard})

export const CtStoreIssueRequestListView = {
    ...listView,
    Renderer: CtStoreIssueRequestDashBoardRenderer,
};

registry.category("views").add("ct_store_issue_request_list", CtStoreIssueRequestListView);
