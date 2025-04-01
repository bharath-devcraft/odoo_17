/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmTenderContractDashBoard } from '@cm_tender_contract/views/cm_tender_contract_dashboard';

export class CmTenderContractDashBoardRenderer extends ListRenderer {};

CmTenderContractDashBoardRenderer.template = 'cm_tender_contract.CmTenderContractListView';
CmTenderContractDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmTenderContractDashBoard})

export const CmTenderContractListView = {
    ...listView,
    Renderer: CmTenderContractDashBoardRenderer,
};

registry.category("views").add("cm_tender_contract_list", CmTenderContractListView);
