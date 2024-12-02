/** @odoo-module **/
 
import { registry } from "@web/core/registry";
 
// Access the user menu registry
const userMenuRegistry = registry.category("user_menuitems");
 
// Remove all items except "log_out"
userMenuRegistry.remove("documentation");
userMenuRegistry.remove("support");
userMenuRegistry.remove("shortcuts");
userMenuRegistry.remove("separator");
userMenuRegistry.remove("odoo_account");
