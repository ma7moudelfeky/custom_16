""" Initialize Model """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class SaleOrder(models.Model):
    """
        Inherit Sale Order:
         -
    """
    _inherit = 'sale.order'

    tax_no = fields.Selection(
        related='partner_id.tax_no'
    )

    def check_tax(self):
        """ Check Tax """
        for rec in self:
            if rec.tax_no == 'no':
                rec.order_line.write({
                    'tax_id': None
                })