
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    """Class for the inherited transient model res.config.settings."""
    _inherit = 'res.config.settings'

    reminder_sales = fields.Boolean(string='Reminder for Sales',
                                    help='Enable this field to get reminder '
                                         'of due in Sale Order.',
                                    config_parameter='sale_invoice_due_date_reminder.reminder_sale')
    set_date_sales = fields.Integer(string='Set Days',
                                    help='Reminder will send according to this '
                                         'number of days set in this field.',
                                    config_parameter='sale_invoice_due_date_reminder.set_date_sales')

    reminder_invoicing = fields.Boolean(string='Reminder for Invoicing',
                                        help='Enable this field to get '
                                             'reminder of due in Invoicing.',
                                        config_parameter='sale_invoice_due_date_reminder.reminder_invoicing')
    set_date_invoicing = fields.Integer(string='Set Days',
                                        help='Reminder will send according to '
                                             'this number of days set in this '
                                             'field.',
                                        config_parameter='sale_invoice_due_date_reminder.set_date_invoicing')
