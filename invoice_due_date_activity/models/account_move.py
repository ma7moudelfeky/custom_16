from datetime import timedelta
from odoo import fields, models


class AccountMove(models.Model):
    """Class for the inherited model account. move"""
    _inherit = 'account.move'

    def action_send_mail_invoice(self):
        """Function for sending mail by checking date in settings. """
        values = self.env['res.config.settings'].default_get(
            list(self.env['res.config.settings'].fields_get()))
        if values['reminder_invoicing'] is not False:
            for record in self.search([]):
                if record.invoice_date_due and record.move_type == 'out_invoice':
                    if record.state == 'draft':
                        if record.invoice_date_due == timedelta(int(values[
                                                                        'set_date_invoicing'])) + fields.Date.today():
                            # mail_template = self.env.ref(
                            #     'sale_invoice_due_date_reminder.invoice_due_mail_template')
                            # mail_template.send_mail(record.id, force_send=True)
                            amount = record.amount_residual
                            date = record.invoice_date
                            customer = record.partner_id.name
                            summary = f"Due Amount :{amount}, By Date : {date}, For Customer : {customer}."
                            group_id = self.env.ref('invoice_due_date_activity.group_activity_for_due_invoices')
                            self.env['user.notify'].create_activity(record, group_id.users, summary)
                    elif record.state == 'posted' and record.payment_state != 'paid' and record.invoice_date_due == timedelta(
                            int(values[
                                    'set_date_invoicing'])) + fields.Date.today():
                        amount = record.amount_residual
                        date = record.invoice_date
                        customer = record.partner_id.name
                        summary = f"Due Amount :{amount}, By Date : {date}, For Customer : {customer}."
                        group_id = self.env.ref('invoice_due_date_activity.group_activity_for_due_invoices')
                        self.env['user.notify'].create_activity(record, group_id.users, summary)
