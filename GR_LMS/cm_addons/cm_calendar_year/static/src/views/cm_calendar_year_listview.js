/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { CmCalendarYearDashBoard } from '@cm_calendar_year/views/cm_calendar_year_dashboard';

export class CmCalendarYearDashBoardRenderer extends ListRenderer {};

CmCalendarYearDashBoardRenderer.template = 'cm_calendar_year.CmCalendarYearListView';
CmCalendarYearDashBoardRenderer.components= Object.assign({}, ListRenderer.components, { CmCalendarYearDashBoard})

export const CmCalendarYearListView = {
    ...listView,
    Renderer: CmCalendarYearDashBoardRenderer,
};

registry.category("views").add("cm_calendar_year_list", CmCalendarYearListView);
