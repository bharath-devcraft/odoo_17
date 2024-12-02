/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmGrHolidayDashBoard } from '@cm_gr_holiday/views/cm_gr_holiday_dashboard';

export class CmGrHolidayDashBoardRenderer extends ListRenderer {};

CmGrHolidayDashBoardRenderer.template = 'cm_gr_holiday.CmGrHolidayListView';
CmGrHolidayDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmGrHolidayDashBoard})

export const CmGrHolidayListView = {
    ...listView,
    Renderer: CmGrHolidayDashBoardRenderer,
};

registry.category("views").add("cm_gr_holiday_list", CmGrHolidayListView);
