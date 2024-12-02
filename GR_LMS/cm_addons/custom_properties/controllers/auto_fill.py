from odoo import http
from odoo.http import request


class AutoFill(http.Controller):
    @http.route(['/matching/records'], type='json', auth="none")
    def get_matching_records(self, **kwargs):
        model = str(kwargs.get('model', ''))
        field = str(kwargs.get('field', ''))
        value = str(kwargs.get('value', ''))
        rec_id = str(kwargs.get('id', ''))
        model = model.replace(".", "_")
        cr = request.cr
        if rec_id:
            rec="and id != %s" % rec_id
        else:
            rec=''
        if len(value.strip()) > 0:
            query = """SELECT %s FROM %s WHERE %s ILIKE %s %s GROUP BY %s""" % (
                field, model, field, "'%s%%'" % value.strip(), rec, field)
            cr.execute(query)
            res = cr.fetchall()
        else:
            res = []
        return res

