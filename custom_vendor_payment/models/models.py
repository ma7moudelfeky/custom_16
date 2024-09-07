# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    send_notification_before = fields.Float(string='Send Notification Before')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            send_notification_before=params.get_param('custom_vendor_payment.send_notification_before'),
        )
        return res

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('custom_vendor_payment.send_notification_before',
                                                  self.send_notification_before)
        return res


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    is_checked = fields.Boolean(string='Check For Payment')


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    check_no = fields.Char(string='Check Number')
    check_due_date = fields.Date(string='Check Due Date')
    bank_id = fields.Many2one('res.bank', string='Check Bank')
    is_true = fields.Boolean(string='تم تحصيله-سداده')
    journal_checked = fields.Boolean()

    @api.onchange('journal_id', 'payment_method_line_id')
    def onchange_journal_checked(self):
        for rec in self:
            if rec.journal_id:
                rec.journal_checked = rec.journal_id.is_checked

    def _action_payment_activity(self):

        payments = self.search([('check_due_date', '>', date.today())])
        send_notification_before = self.env['ir.config_parameter'].sudo().get_param(
            'custom_vendor_payment.send_notification_before')
        activity_type = self.env['mail.activity.type'].create({
            'name': 'To Do',
        })

        group = self.env.ref('custom_vendor_payment.payment_admin')
        users = group.users

        for p in payments:
            for user in users:
                remaining_days = 0
                remaining_days = (p.check_due_date - date.today()).days
                if float(remaining_days) == float(send_notification_before):
                    self.env['mail.activity'].create({
                        'activity_type_id': activity_type.id,
                        'summary': 'برجاء مراجعة تاريخ استحقاق الشيك',
                        'note': 'برجاء مراجعة تاريخ استحقاق الشيك',
                        'user_id': user.id,
                        'res_id': p.id,
                        'res_model_id': self.env.ref('account.model_account_payment').id,
                    })
