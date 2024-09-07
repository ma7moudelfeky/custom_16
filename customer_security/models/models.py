# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    allowed_user_ids = fields.Many2many('res.users', string='Allowed Users')


class ResUsers(models.Model):
    _inherit = 'res.users'

    allowed_partner_ids = fields.Many2many(comodel='res.partner', string='Allowed Partners',
                                           relation="user_partner_rel")

    @api.constrains('allowed_partner_ids')
    def onchange_partner_ids(self):
        self.clear_caches()


class AccountMove(models.Model):
    _inherit = 'account.move'

    allowed_user_ids = fields.Many2many(comodel='res.users', string='Allowed Users',
                                        related='partner_id.allowed_user_ids')


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    allowed_user_ids = fields.Many2many(comodel='res.users', string='Allowed Users',
                                        related='partner_id.allowed_user_ids')

class SalesOrder(models.Model):
    _inherit = 'sale.order'

    allowed_user_ids = fields.Many2many(comodel='res.users', string='Allowed Users',
                                        related='partner_id.allowed_user_ids')
