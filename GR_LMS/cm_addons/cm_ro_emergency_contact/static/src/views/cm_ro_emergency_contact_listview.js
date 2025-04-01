/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmRoEmergencyContactDashBoard } from '@cm_ro_emergency_contact/views/cm_ro_emergency_contact_dashboard';

export class CmRoEmergencyContactDashBoardRenderer extends ListRenderer {};

CmRoEmergencyContactDashBoardRenderer.template = 'cm_ro_emergency_contact.CmRoEmergencyContactListView';
CmRoEmergencyContactDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmRoEmergencyContactDashBoard})

export const CmRoEmergencyContactListView = {
    ...listView,
    Renderer: CmRoEmergencyContactDashBoardRenderer,
};

registry.category("views").add("cm_ro_emergency_contact_list", CmRoEmergencyContactListView);
