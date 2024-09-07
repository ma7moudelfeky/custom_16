# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    commission_ratio = fields.Float(string='Commission Ratio')
    based_on = fields.Selection([('amount', 'Amount Payment'), ('after_first_commission', 'After First Commission')],
                                string='Based On')


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    commission = fields.Boolean(string='Commission', default=False)
    user_id = fields.Many2one('res.users', string='Sales Person')
    team_id = fields.Many2one('crm.team', string='Sales Team')
    user_id_commission = fields.Float(string='Sales Person Commission Ratio')
    user_id_based_on = fields.Selection(
        [('amount', 'Amount Payment'), ('after_first_commission', 'After First Commission')],
        string='Sales Person Based On')
    user_id_commission_value = fields.Monetary(string='Sales Person Commission Value')
    user_id_net = fields.Monetary(string='Sales Person Net')
    team_id_net = fields.Monetary(string='Sales Team Net')
    team_id_commission = fields.Float(string='Sales Team Commission Ratio')
    team_id_based_on = fields.Selection(
        [('amount', 'Amount Payment'), ('after_first_commission', 'After First Commission')],
        string='Sales Team Based On')
    team_id_commission_value = fields.Monetary(string='Sales Team Commission Value')
    commission_type = fields.Selection([
        ('payment', 'Payment'),
        ('sales', 'Sales Order'),
        ('invoices', 'Invoices'),
    ], 'Commission Type',)

    def action_post(self):
        res = super(AccountPayment, self).action_post()
        self.commission_type = self.env['ir.config_parameter'].sudo().get_param(
            'commission_management.commission_type')
        if self.commission_type == 'payment':
            if self.partner_type == 'customer':
                self.commission = True
        if self.partner_id:
            if self.partner_id.user_id or self.partner_id.team_id:
                self.user_id = self.partner_id.user_id
                self.team_id = self.partner_id.team_id
                self.user_id_commission = self.user_id.partner_id.commission_ratio
                self.user_id_based_on = self.user_id.partner_id.based_on
                self.team_id_commission = self.team_id.user_id.partner_id.commission_ratio
                self.team_id_based_on = self.team_id.user_id.partner_id.based_on
                if self.user_id_based_on == 'amount':
                    self.user_id_net = self.amount - (self.amount * self.user_id_commission)
                    self.user_id_commission_value = self.amount * self.user_id_commission
                if self.team_id_based_on == 'amount':
                    self.team_id_net = self.amount - (self.amount * self.team_id_commission)
                elif self.team_id_based_on == 'after_first_commission':
                    self.team_id_net = self.user_id_net - (self.user_id_net * self.team_id_commission)
                    self.team_id_commission_value = self.user_id_net * self.team_id_commission
        return res


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    commission_type = fields.Selection([
        ('payment', 'Payment'),
        ('sales', 'Sales Order'),
        ('invoices', 'Invoices'),
    ], 'Commission Type',
        default='payment')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            commission_type=params.get_param('commission_management.commission_type'),
        )
        return res

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('commission_management.commission_type',
                                                  self.commission_type)
        return res


