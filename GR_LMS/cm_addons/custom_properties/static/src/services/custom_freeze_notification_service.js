/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { browser } from "@web/core/browser/browser";
import { ConnectionLostError } from "@web/core/network/rpc_service";
import { registry } from "@web/core/registry";

export const CustomFreezeNotificationService = {
    dependencies: ["action", "bus_service", "notification", "rpc"],

    start(env, { action, bus_service, notification, rpc }) {
        let CustomFreezeNotifTimeouts = {};
        let nextCustomFreezeNotifTimeout = null;
        const displayedNotifications = new Set();
        bus_service.subscribe("custom.freeze.notification", (payload) => {
            displayCustomFreezeNotification(payload);
        });
        bus_service.start();

        function displayCustomFreezeNotification(notifications) {
            let lastNotifTimer = 0;

            browser.clearTimeout(nextCustomFreezeNotifTimeout);
            Object.values(CustomFreezeNotifTimeouts).forEach((notif) => browser.clearTimeout(notif));
            CustomFreezeNotifTimeouts = {};

            notifications.forEach(function (notif) {
                const key = notif.user_id;
                if (displayedNotifications.has(key)) {
                    return;
                }
                
                CustomFreezeNotifTimeouts[key] = browser.setTimeout(function () {
                    const notificationRemove = notification.add(notif.message, {
                        title: notif.title,
                        type: "danger",
                        sticky: true,
                        onClose: () => {
                            displayedNotifications.delete(key);
                            if (notif.close === 'yes') {
                                browser.clearTimeout(autoCloseTimeout);
                            }
                        },
                        buttons: [
                            {
                                name: _t("OK"),
                                primary: true,
                                onClick: async () => {
                                    //await rpc("/ct_transaction/notify_ack");
                                    notificationRemove();
                                },
                            },
                            //~ {
                                //~ name: _t("Details"),
                                //~ onClick: async () => {
                                    //~ await action.doAction({
                                        //~ type: 'ir.actions.act_window',
                                        //~ res_model: 'ct.transaction',
                                        //~ res_id: notif.event_id,
                                        //~ views: [[false, 'form']],
                                    //~ });
                                    //~ notificationRemove();
                                //~ },
                            //~ },
                            //~ {
                                //~ name: _t("Snooze"),
                                //~ onClick: () => {
                                    //~ notificationRemove();
                                //~ },
                            //~ },
                            {
                                name: _t("Stop"),
                                onClick: async () => {
                                    await rpc("/custom/popup/disable", {
                                        user_id: notif.user_id,
                                        notify_name: notif.notify_name,
                                    });
                                    notificationRemove();
                                },
                            },
                        ],
                    });
                    displayedNotifications.add(key);
                    
                    let autoCloseTimeout;
                    if (notif.close === 'yes') {
                        // Auto-close notification after 10 minutes
                        const autoCloseTimeout = browser.setTimeout(() => {
                            notificationRemove();
                        }, 10000); // 600,000 milliseconds = 10 minutes
                    }


                }, notif.timer * 1000);
                lastNotifTimer = Math.max(lastNotifTimer, notif.timer);
            });

            //~ if (lastNotifTimer > 0) {
                //~ nextCtTransactionNotifTimeout = browser.setTimeout(
                    //~ getNextCtTransactionNotif,
                    //~ lastNotifTimer * 1000
                //~ );
            //~ }
        }

        //~ async function getNextCtTransactionNotif() {
            //~ try {
                //~ const result = await rpc("/ct_transaction/notify", {}, { silent: true });
                //~ displayCtTransactionNotification(result);
            //~ } catch (error) {
                //~ if (!(error instanceof ConnectionLostError)) {
                    //~ throw error;
                //~ }
            //~ }
        //~ }
    },
};

registry.category("services").add("CustomFreezeNotification", CustomFreezeNotificationService);
