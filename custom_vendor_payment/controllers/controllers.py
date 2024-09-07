# -*- coding: utf-8 -*-
# from odoo import http


# class CustomVendorPayment(http.Controller):
#     @http.route('/custom_vendor_payment/custom_vendor_payment', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_vendor_payment/custom_vendor_payment/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_vendor_payment.listing', {
#             'root': '/custom_vendor_payment/custom_vendor_payment',
#             'objects': http.request.env['custom_vendor_payment.custom_vendor_payment'].search([]),
#         })

#     @http.route('/custom_vendor_payment/custom_vendor_payment/objects/<model("custom_vendor_payment.custom_vendor_payment"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_vendor_payment.object', {
#             'object': obj
#         })
