# -*- coding: utf-8 -*-
# from odoo import http


# class CustomerSecurity(http.Controller):
#     @http.route('/customer_security/customer_security', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/customer_security/customer_security/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('customer_security.listing', {
#             'root': '/customer_security/customer_security',
#             'objects': http.request.env['customer_security.customer_security'].search([]),
#         })

#     @http.route('/customer_security/customer_security/objects/<model("customer_security.customer_security"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('customer_security.object', {
#             'object': obj
#         })
