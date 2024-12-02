# -*- coding: utf-8 -*-
# from odoo import http


# class CmDivisionMaster(http.Controller):
#     @http.route('/cm_division_master/cm_division_master', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cm_division_master/cm_division_master/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('cm_division_master.listing', {
#             'root': '/cm_division_master/cm_division_master',
#             'objects': http.request.env['cm_division_master.cm_division_master'].search([]),
#         })

#     @http.route('/cm_division_master/cm_division_master/objects/<model("cm_division_master.cm_division_master"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cm_division_master.object', {
#             'object': obj
#         })

