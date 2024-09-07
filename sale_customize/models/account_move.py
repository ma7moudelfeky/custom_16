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

    first_use = fields.Boolean(
        copy=0
    )
    second_use = fields.Boolean(
        copy=0
    )
    all_amount = fields.Float(
        compute='_compute_all_amount'
    )
    first_discount_amount = fields.Float(
        copy=0
    )
    whole_discount_id = fields.Many2one(
        'whole.discount'
    )

    @api.depends('invoice_line_ids')
    def _compute_all_amount(self):
        """ Compute all_amount value """
        for rec in self:
            if rec.invoice_line_ids:
                rec.all_amount = sum(rec.invoice_line_ids.mapped('all_amount')) + rec.amount_tax
            else:
                rec.all_amount = 0


class AccountMoveLine(models.Model):
    """
        Inherit Account Move Line:
         -
    """
    _inherit = 'account.move.line'

    all_amount = fields.Float(
        compute='_compute_all_amount'
    )

    @api.depends('price_unit', 'quantity')
    def _compute_all_amount(self):
        """ Compute all_amount value """
        for rec in self:
            rec.all_amount = rec.price_unit * rec.quantity