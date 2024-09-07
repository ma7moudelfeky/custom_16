""" Initialize Account Move Report """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning
class CustomInvoiceReport(models.AbstractModel):
    _name = 'report.account_move_report.report_invoice'
    _description = 'Custom Invoice Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['account.move.line'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'account.move',
            'docs': docs,
        }