from odoo import fields, models

class ShMessageWizard(models.TransientModel):
    _name = "sh.message.wizard"
    _description = "Message wizard to display warnings, alert ,success messages"

    def get_default(self):
        if self.env.context.get("message", False):
            return self.env.context.get("message")
        return False

    def get_id_default(self):
        if self.env.context.get("transaction_id",False):
            return self.env.context.get("transaction_id")
        return False 
        
    def get_model_default(self):
        if self.env.context.get("transaction_model",False):
            return self.env.context.get("transaction_model")
        return False 
        
    def get_stage_default(self):
        if self.env.context.get("transaction_stage",False):
            return self.env.context.get("transaction_stage")
        return False 

    def get_flag_default(self):
        if self.env.context.get("transaction_flag",False):
            return self.env.context.get("transaction_flag")
        return False 

    name=fields.Text(string="Message",readonly=True,default=get_default)
    transaction_id=fields.Integer(string="ID",readonly=True,default=get_id_default)
    transaction_model=fields.Char(string="Model",readonly=True,default=get_model_default)
    transaction_stage = fields.Char(string="Stage",readonly=True,default=get_stage_default)

    def entry_cancel(self):
        return True

    def entry_confirm(self):
        transaction_model_methods = {
            'ct.transaction': {'wfa': 'entry_approve'},
            'cm.master': {'draft': 'entry_approve', 'editable': 'entry_approve'},
            'cm.profile.master': {'draft': 'entry_approve', 'editable': 'entry_approve'},
            'cm.fiscal.year': {'draft': 'entry_approve', 'editable': 'entry_approve'},
            'cm.supplier.customer': {'draft': 'entry_approve', 'editable': 'entry_approve'}
        }
        
        # Check if the current transaction model and stage are defined in the mapping
        stage_methods = transaction_model_methods.get(self.transaction_model, {})
        method_name = stage_methods.get(self.transaction_stage)

        if method_name:
            transaction_rec = self.env[self.transaction_model].browse(self.transaction_id)
            # Call the method dynamically
            getattr(transaction_rec, method_name)()

        return True
