from odoo import api, models, fields

def users_search(env):
    users_rec = env['res.users']
    users = users_rec.search([])
    return users
   
def users_details():
    # Create the Odoo environment
    from odoo import api, SUPERUSER_ID
    from odoo.modules.registry import Registry
    registry = Registry.new('odoo17')
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        # Call the custom function and pass the Odoo environment ('env')
        return ", ".join([str(users.login) for users in users_search(env) if users])
