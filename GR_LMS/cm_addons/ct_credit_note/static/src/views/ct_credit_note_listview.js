/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CtCreditNoteDashBoard } from '@ct_credit_note/views/ct_credit_note_dashboard';

export class CtCreditNoteDashBoardRenderer extends ListRenderer {};

CtCreditNoteDashBoardRenderer.template = 'ct_credit_note.CtCreditNoteListView';
CtCreditNoteDashBoardRenderer.components= Object.assign({}, ListRenderer.components, {CtCreditNoteDashBoard})

export const CtCreditNoteListView = {
    ...listView,
    Renderer: CtCreditNoteDashBoardRenderer,
};

registry.category("views").add("ct_credit_note_list", CtCreditNoteListView);
