/** @odoo-module */
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart } from "@odoo/owl";

export class CtCreditNoteDashBoard extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");

        onWillStart(async () => {
            this.transactionData = await this.orm.call("ct.credit.note", "retrieve_dashboard");
        });
    }

    setSearchContext(ev) {
        const filter_name = ev.currentTarget.getAttribute("filter_name");
        const filters = filter_name.split(",");
        const searchItems = this.env.searchModel.getSearchItems((item) =>
            filters.includes(item.name)
        );
        this.env.searchModel.query = [];
        for (const item of searchItems) {
            this.env.searchModel.toggleSearchItem(item.id);
        }
    }

    stopMarquee(ev) {
        ev.currentTarget.stop();
    }

    startMarquee(ev) {
        ev.currentTarget.start();
    }
    
}

CtCreditNoteDashBoard.template = "ct_credit_note.CtCreditNoteDashBoard";
