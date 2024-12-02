# -*- coding: utf-8 -*-
# from odoo import http


# class TravelPackageMaster(http.Controller):
#     @http.route('/travel_package_master/travel_package_master', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/travel_package_master/travel_package_master/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('travel_package_master.listing', {
#             'root': '/travel_package_master/travel_package_master',
#             'objects': http.request.env['travel_package_master.travel_package_master'].search([]),
#         })

#     @http.route('/travel_package_master/travel_package_master/objects/<model("travel_package_master.travel_package_master"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('travel_package_master.object', {
#             'object': obj
#         })
