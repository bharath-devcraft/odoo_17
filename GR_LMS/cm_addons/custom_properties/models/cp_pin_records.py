from odoo import api, fields, models


class CpPinRecord(models.Model):
    """Class is used to store pinned recodes in the database"""
    _name = 'cp.pin.records'
    _description = 'Pin Records'

    record_id = fields.Integer(string="Record Id", help='Record id')
    res_model = fields.Char(string="Model", help='Corresponding model')
    color = fields.Char(string="Color", help='Color code')
    user_id = fields.Many2one('res.users', string='User',
                              help="Set current user")

    @api.model
    def save_pin_record(self, pin_model):
        """Function to fetch data from XML"""
        record = self.search([('record_id', '=', pin_model[0]), ('res_model', '=', pin_model[1])])
        if record:
            record.unlink()
        else:
            self.create({
                'record_id': pin_model[0],
                'res_model': pin_model[1],
                'color': pin_model[2],
                'user_id': self.env.uid
            })
        result = self.search([('res_model', '=', pin_model)])
        return result

    @api.model
    def pin_record(self, pin_model):
        """Function to fetch id and color of the specified model"""
        pinned_record = []
        record_ids = self.search([('res_model', '=', pin_model),
                                  ('user_id', '=', self.env.uid)])
        for record_id in record_ids:
            pinned_record.append({
                'id': record_id.record_id,
                'color': record_id.color,
                'model': record_id.res_model
            })
        return pinned_record
