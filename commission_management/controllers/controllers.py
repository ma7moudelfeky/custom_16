# -*- coding: utf-8 -*-
# from odoo import http


# class CommissionManagement(http.Controller):
#     @http.route('/commission_management/commission_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/commission_management/commission_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('commission_management.listing', {
#             'root': '/commission_management/commission_management',
#             'objects': http.request.env['commission_management.commission_management'].search([]),
#         })

#     @http.route('/commission_management/commission_management/objects/<model("commission_management.commission_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('commission_management.object', {
#             'object': obj
#         })
