/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { browser } from "@web/core/browser/browser";
import { ConnectionLostError } from "@web/core/network/rpc_service";
import { registry } from "@web/core/registry";

export const CustomCloseNotificationService = {
    dependencies: ["action", "bus_service", "notification", "rpc"],

    start(env, { action, bus_service, notification, rpc }) {
        let CustomCloseNotifTimeouts = {};
        const displayedNotifications = new Set();

        bus_service.subscribe("custom.close.notification", (payload) => {
            displayCustomCloseNotification(payload);
        });
        bus_service.start();

        function displayCustomCloseNotification(notifications) {
            notifications.forEach(function (notif) {
                const key = `${notif.user_id}_${notif.notify_name}`;
                if (displayedNotifications.has(key)) {
                    return;
                }

                const notificationRemove = notification.add(notif.message, {
                    title: notif.title,
                    type: notif.close === "yes" ? "info" : "danger",
                    sticky: true,
                    onClose: () => {
                        displayedNotifications.delete(key);
                        if (CustomCloseNotifTimeouts[key]) {
                            browser.clearTimeout(CustomCloseNotifTimeouts[key]);
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

                if (notif.close === 'yes') {
                    CustomCloseNotifTimeouts[key] = browser.setTimeout(() => {
                        notificationRemove();
                        }, 10000); // 600,000 milliseconds = 10 minutes
                }

                displayedNotifications.add(key);
            });
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

registry.category("services").add("CustomCloseNotification", CustomCloseNotificationService);
