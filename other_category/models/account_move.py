""" Initialize Account Move """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class AccountMove(models.Model):
    """
        Inherit Account Move:
         -
    """
    _inherit = 'account.move'

    @api.constrains('invoice_line_ids')
    @api.onchange('invoice_line_ids')
    def _check_invoice_line_ids(self):
        """ Validate invoice_line_ids """
        for rec in self:
            if rec.invoice_line_ids:
                ref = rec.invoice_line_ids.mapped('product_id').mapped('categ_id').filtered(lambda x:x.for_others)
                if ref:
                    rec.ref = ref[0].name