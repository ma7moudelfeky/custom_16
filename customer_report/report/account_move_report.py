""" Initialize Account Move Report """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning

class CustomInvoiceReport(models.AbstractModel):
    _name = 'report.customer_report.report_invoice_template'
    _description = 'Partner Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        data = dict(data or {})
        return data